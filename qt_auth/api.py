from django.contrib.auth import authenticate
from django.db.models import Q
from ninja import Router

from qt_auth.exceptions import JWTDecodeError, UserNotFound
from qt_auth.schemas.auth import ErrorResponse, JWTRefreshTokenInfo, JWTTokenInfo, SignIn, SignUp, StatusOk
from qt_auth.utils import (
    REFRESH_TOKEN_TYPE,
    create_access_token,
    create_refresh_token,
    get_verified_data_from_token,
    is_token_revoked,
    revoke_token,
)
from qt_user.models import User

app = Router()


@app.post("/signup", response={201: StatusOk, 400: ErrorResponse, 409: ErrorResponse})
def signup(request, data: SignUp):
    if User.objects.filter(username=data.username).exists():
        return 409, ErrorResponse(
            code='CONFLICT',
            message='User already exists',
            errors=[{'username': 'Username is already taken'}],
        )

    if User.objects.filter(email=data.email).exists():
        return 409, ErrorResponse(
            code='CONFLICT',
            message='User already exists',
            errors=[{'email': 'Email is already taken'}],
        )

    User.objects.create_user(
        username=data.username,
        password=data.password,
        email=data.email,
    )
    return 201, StatusOk(status="Ok")


@app.post("/signin", response={200: JWTTokenInfo, 400: ErrorResponse, 401: ErrorResponse, 404: ErrorResponse})
def signin(request, data: SignIn):
    is_email_auth = '@' in data.username

    if is_email_auth:
        q = Q(email__iexact=data.username)
    else:
        q = Q(username__iexact=data.username)
    suggested_user = User.objects.filter(q).first()

    if not suggested_user:
        return 404, ErrorResponse(
            code='NOT_FOUND',
            message='User not found',
        )

    authenticated_user = authenticate(username=suggested_user.username, password=data.password)
    if not authenticated_user:
        return 401, ErrorResponse(
            code='UNAUTHORIZED',
            message='Invalid credentials',
        )

    access_token = create_access_token(authenticated_user)
    refresh_token = create_refresh_token(authenticated_user)
    return JWTTokenInfo(access=access_token, refresh=refresh_token)


@app.post("/refresh", response={200: JWTTokenInfo, 400: ErrorResponse, 401: ErrorResponse})
def refresh(request, data: JWTRefreshTokenInfo):
    try:
        refresh_token_payload, user = get_verified_data_from_token(data.refresh)
    except JWTDecodeError as e:
        message = str(e)
        return 401, ErrorResponse(
            code='UNAUTHORIZED',
            message='Invalid jwt token',
            errors=[{'jwt': message}],
        )
    except UserNotFound as e:
        message = str(e)
        return 401, ErrorResponse(
            code='UNAUTHORIZED',
            message='Invalid jwt token',
            errors=[{'user': message}],
        )

    if refresh_token_payload['type'] != REFRESH_TOKEN_TYPE:
        return 401, ErrorResponse(
            code='UNAUTHORIZED',
            message='Invalid jwt token',
            errors=[{'jwt': 'Token type is not refresh'}],
        )

    if is_token_revoked(refresh_token_payload):
        return 401, ErrorResponse(
            code='UNAUTHORIZED',
            message='Invalid jwt token',
            errors=[{'jwt': 'Refresh token has been revoked'}],
        )

    revoke_token(refresh_token_payload)

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return JWTTokenInfo(access=access_token, refresh=refresh_token)
