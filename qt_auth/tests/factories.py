import factory

from qt_user.models import User


class UserFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n + 1)  # noqa: A003
    username = 'test'
    email = 'test@test.com'
    password = factory.django.Password('superpass')

    class Meta:
        model = User
