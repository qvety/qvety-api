from django.db.utils import IntegrityError

from qt_space.logic.exceptions import SpaceConflictError
from qt_user.models import User
from qt_user.schemas.user import UserRequestSchema


class UserServie:
    def __init__(self, user: User):
        self.current_user = user

    def get_current(self) -> User:
        return self.current_user

    def update_current(self, data: UserRequestSchema) -> User:
        for attr, value in data.dict().items():
            setattr(self.current_user, attr, value)
        try:
            self.current_user.save()
        except IntegrityError as e:
            raise SpaceConflictError() from e
        return self.current_user
