from qt_auth.logic.exceptions import UserEmailAlreadyExistsError, UsernameAlreadyExistsError
from qt_auth.schemas.auth import SignUpRequestSchema
from qt_user.models import User


class RegistrationService:

    @staticmethod
    def register_user(data: SignUpRequestSchema) -> User:
        if User.objects.filter(username=data.username).exists():
            raise UsernameAlreadyExistsError()

        if User.objects.filter(email=data.email).exists():
            raise UserEmailAlreadyExistsError()

        user = User.objects.create_user(
            username=data.username,
            password=data.password,
            email=data.email,
        )
        return user
