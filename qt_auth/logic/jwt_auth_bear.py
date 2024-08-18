from ninja.security import HttpBearer

from qt_auth.logic.exceptions import JWTError
from qt_auth.logic.services.jwt_service import JWTService


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        service = JWTService()
        try:
            service.verify_access_token(token)
        except JWTError:
            return None

        return service.get_user()
