from unittest.mock import patch

from django.test import TestCase

from common.tests import AuthenticatedClient
from qt_space.api.rooms import router
from qt_space.tests.factories import UserFactory


class RoomTestCase(TestCase):
    def setUp(self):
        self.client = AuthenticatedClient(router)

        patcher = patch('qt_auth.utils.AuthBearer.authenticate')
        self.mocked_object = patcher.start()
        self.mocked_object.return_value = UserFactory()
        self.addCleanup(patcher.stop)

    def test_create_room(self):
        room_data = {
            'name': 'room #1',
            'temperature': 19,
            'humidity': 23,
        }
        resp = self.client.post('/room', json=room_data)
        self.assertEqual(resp.status_code, 201)
