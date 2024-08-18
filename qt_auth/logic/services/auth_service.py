from django.contrib.auth import authenticate
from django.db.models import Q

from qt_auth.logic.exceptions import InvalidCredentialsError
from qt_auth.logic.services.jwt_service import JWTService
from qt_auth.schemas.auth import SignInResponseSchema
from qt_user.models import User


class AuthService:

    @staticmethod
    def login(data: SignInResponseSchema) -> tuple[str, str]:
        is_email_auth = '@' in data.username

        q = Q(email__iexact=data.username) if is_email_auth else Q(username__iexact=data.username)
        suggested_user = User.objects.filter(q).first()

        if not suggested_user:
            raise InvalidCredentialsError()

        authenticated_user = authenticate(username=suggested_user.username, password=data.password)
        if not authenticated_user:
            raise InvalidCredentialsError()

        jwt_service = JWTService(authenticated_user)
        access_token = jwt_service.create_access_token()
        refresh_token = jwt_service.create_refresh_token()
        return access_token, refresh_token
