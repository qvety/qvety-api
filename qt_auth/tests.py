from django.test import TestCase

from qt_user.models import User
from qt_auth.utils import get_verified_payload_from_token
from datetime import datetime

class SignUpTestCase(TestCase):
    def setUp(self):
        self.signup_url = '/api/auth/signup'

    def test_ok(self):
        user_data = {
            'username': 'test_ok',
            'password': 'superpass',
            'email': '         test@example.com           '
        }
        resp = self.client.post(self.signup_url, data=user_data, content_type='application/json')
        self.assertEqual(resp.status_code, 201)

        data = resp.json()
        self.assertEqual(data['status'], 'Ok')

    def test_email_validation(self):
        user_data = {
            'username': 'test_zalupaka',
            'password': 'superpass',
            'email': '!z@lupka228@gmail.com'
        }
        resp = self.client.post(self.signup_url, data=user_data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)

        data = resp.json()
        self.assertEqual(data['code'], 'BAD_REQUEST')

    def test_set_username(self):
        user_data = {
            'password': 'superpass',
            'email': 'test@gmail.com'
        }
        resp = self.client.post(self.signup_url, data=user_data, content_type='application/json')
        self.assertEqual(resp.status_code, 201)

        user = User.objects.get(username='test')
        self.assertEqual(user.username, 'test')

    def test_exist_creds(self):
        user_data = {
            'password': 'superpass',
            'email': 'test@gmail.com'
        }
        resp = self.client.post(self.signup_url, data=user_data, content_type='application/json')
        self.assertEqual(resp.status_code, 201)

        exist_username = {
            'username': 'test',
            'password': 'superpass',
            'email': 'test1@gmail.com'
        }
        resp = self.client.post(self.signup_url, data=exist_username, content_type='application/json')
        self.assertEqual(resp.status_code, 409)

        data = resp.json()
        self.assertEqual(data['errors'][0]['username'], 'Username is already taken')

        exist_email = {
            'username': 'test1',
            'password': 'superpass',
            'email': 'test@gmail.com'
        }
        resp = self.client.post(self.signup_url, data=exist_email, content_type='application/json')
        self.assertEqual(resp.status_code, 409)

        data = resp.json()
        self.assertEqual(data['errors'][0]['email'], 'Email is already taken')


class SignInTestCase(TestCase):
    def setUp(self):
        self.signin_url = '/api/auth/signin'
        self.base_user_data = {
            'password': 'superpass',
            'username': 'test',
            'email': 'test@test.com',
        }
        self.user = self._create_user(
            username=self.base_user_data['username'],
            password=self.base_user_data['password'],
            email=self.base_user_data['email'],
        )

    @staticmethod
    def _create_user(username, password, email):
        return User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

    def test_ok(self):
        user_data = {
            'password': 'superpass',
            'username': 'test',
        }
        resp = self.client.post(self.signin_url, data=user_data, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertIn('access', data)
        self.assertIn('refresh', data)

    def test_login_by_email(self):
        user_data = {
            'password': 'superpass',
            'username': 'test@test.com',
        }
        resp = self.client.post(self.signin_url, data=user_data, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertIn('access', data)
        self.assertIn('refresh', data)

    def test_not_exist_user(self):
        user_data = {
            'password': 'superpass',
            'username': 'fake@test.com',
        }
        resp = self.client.post(self.signin_url, data=user_data, content_type='application/json')
        self.assertEqual(resp.status_code, 404)

        data = resp.json()
        self.assertEqual(data['message'], 'User not found')

    def test_wrong_password(self):
        user_data = {
            'password': 'zalupka228',
            'username': 'test',
        }
        resp = self.client.post(self.signin_url, data=user_data, content_type='application/json')
        self.assertEqual(resp.status_code, 401)

        data = resp.json()
        self.assertEqual(data['message'], 'Invalid credentials')

    def test_token_data(self):
        user_data = {
            'password': 'superpass',
            'username': 'test',
        }
        resp = self.client.post(self.signin_url, data=user_data, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        access, refresh = data['access'], data['refresh']
        verified_payload_access = get_verified_payload_from_token(access)
        verified_payload_refresh = get_verified_payload_from_token(refresh)
        fifteen_minutes_timestamp = datetime.now().timestamp() + 60 * 1
        one_day_timestamp = datetime.now().timestamp() + 30 * 24 * 60 * 60

        self.assertLess(verified_payload_access['exp'], fifteen_minutes_timestamp)
        self.assertEqual(verified_payload_access['user_id'], self.user.id)
        self.assertEqual(verified_payload_access['type'], 'access')

        self.assertLess(verified_payload_refresh['exp'], one_day_timestamp)
        self.assertLess(fifteen_minutes_timestamp, verified_payload_refresh['exp'])
        self.assertEqual(verified_payload_refresh['user_id'], self.user.id)
        self.assertEqual(verified_payload_refresh['type'], 'refresh')
