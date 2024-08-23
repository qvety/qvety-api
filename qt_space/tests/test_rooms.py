from unittest.mock import patch

from django.test import TestCase

from qt_space.tests.factories import RoomFactory, UserFactory


class RoomTestCase(TestCase):
    def setUp(self):
        # With ninja.testing.TestClient exc handler doesn't work
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer Test'

        self.user = UserFactory()
        self.room = RoomFactory(user=self.user)

        patcher = patch('qt_auth.logic.jwt_auth_bear.AuthBearer.authenticate')
        self.mocked_object = patcher.start()
        self.mocked_object.return_value = self.user
        self.addCleanup(patcher.stop)

    def test_create_room(self):
        room_data = {
            'name': 'room #1',
            'temperature': 19,
            'humidity': 23,
        }

        resp = self.client.post('/api/space/room', data=room_data, content_type='application/json')
        self.assertEqual(resp.status_code, 201)

    def test_invalid_create_room(self):
        room_data = {
            'name': 'room #1',
            'temperature': -10000,
            'humidity': 23,
        }
        resp = self.client.post('/api/space/room', data=room_data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)

        data = resp.json()
        self.assertEqual(data['errors'][0]['temperature'], 'Input should be greater than or equal to -273')

    def test_get_room(self):
        resp = self.client.get('/api/space/rooms')

        data = resp.json()
        self.assertNotEqual(len(data), 0)

        obj_uuid = data[-1].get('uuid')
        self.assertIsNotNone(obj_uuid)

        resp = self.client.get(f'/api/space/room/{obj_uuid}')

        data = resp.json()
        self.assertEqual(data['uuid'], str(self.room.uuid))
        self.assertEqual(data['name'], self.room.name)

        resp = self.client.get('/api/space/room/995b5156-9e9d-4b64-8a44-a150d79af4b8')

        data = resp.json()
        self.assertEqual(data['detail'], 'Not found')

    def test_update_room(self):
        self.assertEqual(self.room.name, 'factory room')
        room_data = {
            'name': 'new room #1',
            'temperature': 15,
            'humidity': 23,
        }
        uid = str(self.room.uuid)
        resp = self.client.put(f'/api/space/room/{uid}', data=room_data, content_type='application/json')
        self.assertEqual(resp.status_code, 201)

        data = resp.json()
        self.assertEqual(room_data['name'], data['name'])

    def test_delete_room(self):
        uid = str(self.room.uuid)
        resp = self.client.delete(f'/api/space/room/{uid}', content_type='application/json')
        self.assertEqual(resp.status_code, 204)
