import uuid

import factory

from qt_space.models import Space
from qt_user.models import User


class UserFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n + 1)  # noqa: A003
    username = factory.Sequence(lambda n: f'test_user_{n}')
    email = factory.Sequence(lambda n: f"test_user_{n}@qt.com")

    class Meta:
        model = User


class RoomFactory(factory.django.DjangoModelFactory):
    uuid = uuid.uuid4()
    name = 'factory room'
    user: User

    class Meta:
        model = Space
