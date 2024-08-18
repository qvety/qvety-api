from django.http import HttpRequest
from ninja import Router

from common.exceptions import BaseQtError
from common.http_response import QtORJSONResponse
from common.schemas import ErrorResponse
from qt_auth.logic.services.auth_service import AuthService
from qt_auth.logic.services.jwt_service import JWTService
from qt_auth.logic.services.registration_service import RegistrationService
from qt_auth.schemas.auth import (
    JWTRefreshTokenSchema,
    JWTTokenSchema,
    SignInResponseSchema,
    SignUpRequestSchema,
    SignUpResponseSchema,
)

router = Router()


@router.post(
    path="/signup",
    response={
        201: SignUpResponseSchema,
        (400, 409): ErrorResponse,
    },
)
def signup(request: HttpRequest, data: SignUpRequestSchema) -> QtORJSONResponse:
    try:
        user = RegistrationService.register_user(data)
    except BaseQtError as e:
        return e.to_response()

    return QtORJSONResponse(
        data=SignUpResponseSchema(username=user.username).model_dump(),
        status=201,
    )


@router.post(
    path="/signin",
    response={
        200: JWTTokenSchema,
        (400, 401, 404): ErrorResponse,
    },
)
def signin(request: HttpRequest, data: SignInResponseSchema) -> QtORJSONResponse:
    try:
        access_token, refresh_token = AuthService.login(data)
    except BaseQtError as e:
        return e.to_response()

    return QtORJSONResponse(
        data=JWTTokenSchema(access=access_token, refresh=refresh_token).model_dump(),
        status=200,
    )


@router.post(
    path="/refresh",
    response={
        200: JWTTokenSchema,
        (400, 401): ErrorResponse,
    },
)
def refresh(request: HttpRequest, data: JWTRefreshTokenSchema) -> QtORJSONResponse:
    service = JWTService()
    try:
        service.verify_refresh_token(data.refresh)
    except BaseQtError as e:
        return e.to_response()

    access_token = service.create_access_token()
    refresh_token = service.create_refresh_token()
    return QtORJSONResponse(
        data=JWTTokenSchema(access=access_token, refresh=refresh_token).model_dump(),
        status=200,
    )
