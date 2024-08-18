from uuid import UUID

from django.db.models import QuerySet
from django.db.utils import IntegrityError

from qt_space.logic.exceptions import SpaceConflictError, SpaceNotFoundError
from qt_space.models import Space
from qt_space.schemas.space import RoomRequestSchema
from qt_user.models import User


class RoomsServie:
    def __init__(self, user: User):
        self.current_user = user

    def get(self, uid: UUID) -> Space:
        qs = Space.objects.filter(uuid=uid, user=self.current_user)
        try:
            return qs.get()
        except Space.DoesNotExist as e:
            raise SpaceNotFoundError() from e

    def create(self, data: RoomRequestSchema) -> Space:
        room = Space(
            name=data.name,
            description=data.description,
            user=self.current_user,
            hemisphere=data.hemisphere,
            temperature=data.temperature,
            humidity=data.humidity,
            window_side=data.window_side,
        )
        try:
            room.save()
        except IntegrityError as e:
            raise SpaceConflictError() from e
        return room

    def get_list(self) -> QuerySet[Space]:
        return Space.objects.filter(user=self.current_user).all()

    def update(self, uid: UUID, data: RoomRequestSchema) -> Space:
        room = self.get(uid)
        for attr, value in data.dict().items():
            setattr(room, attr, value)
        try:
            room.save()
        except IntegrityError as e:
            raise SpaceConflictError() from e
        return room

    def delete(self, uid: UUID) -> None:
        room = self.get(uid)
        room.delete()
