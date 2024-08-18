from django.test import TestCase
from ninja.testing import TestClient

from qt_auth.api.auth import router
from qt_user.models import User


class SignUpTestCase(TestCase):
    def setUp(self):
        self.client = TestClient(router)
        self.signup_url = '/signup'

    def test_ok(self):
        username = 'test_ok'
        user_data = {
            'username': username,
            'password': 'superpass',
            'email': '         test@example.com           '
        }
        resp = self.client.post(self.signup_url, json=user_data)
        self.assertEqual(resp.status_code, 201)

        data = resp.json()
        self.assertEqual(data['username'], username)

    def test_email_validation(self):
        user_data = {
            'username': 'test_zalupaka',
            'password': 'superpass',
            'email': '!z@lupka228@gmail.com'
        }
        resp = self.client.post('/signup', json=user_data)
        self.assertNotEqual(resp.status_code, 201)

    def test_set_username(self):
        user_data = {
            'password': 'superpass',
            'email': 'test@gmail.com'
        }
        resp = self.client.post(self.signup_url, json=user_data)
        self.assertEqual(resp.status_code, 201)

        user = User.objects.get(username='test')
        self.assertEqual(user.username, 'test')

    def test_exist_creds(self):
        user_data = {
            'password': 'superpass',
            'email': 'test@gmail.com'
        }
        resp = self.client.post(self.signup_url, json=user_data)
        self.assertEqual(resp.status_code, 201)

        exist_username = {
            'username': 'test',
            'password': 'superpass',
            'email': 'test1@gmail.com'
        }
        resp = self.client.post(self.signup_url, json=exist_username)
        self.assertEqual(resp.status_code, 409)

        data = resp.json()
        self.assertEqual(data['detail'], 'Username is already taken')

        exist_email = {
            'username': 'test1',
            'password': 'superpass',
            'email': 'test@gmail.com'
        }
        resp = self.client.post(self.signup_url, json=exist_email)
        self.assertEqual(resp.status_code, 409)

        data = resp.json()
        self.assertEqual(data['detail'], 'Email is already taken')
