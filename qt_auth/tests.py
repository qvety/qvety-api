from datetime import datetime
from unittest.mock import patch

from django.test import TestCase

from qt_auth.utils import create_access_token, create_refresh_token, get_verified_payload_from_token
from qt_user.models import User


def _create_user(username, password, email):
    return User.objects.create_user(
        username=username,
        password=password,
        email=email,
    )


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
        self.user = _create_user(
            username=self.base_user_data['username'],
            password=self.base_user_data['password'],
            email=self.base_user_data['email'],
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


class RefreshTokenTestCase(TestCase):
    def setUp(self):
        self.signin_url = '/api/auth/signin'
        self.refresh_url = '/api/auth/refresh'
        self.base_user_data = {
            'password': 'superpass',
            'username': 'test',
            'email': 'test@test.com',
        }
        self.user = _create_user(
            username=self.base_user_data['username'],
            password=self.base_user_data['password'],
            email=self.base_user_data['email'],
        )
        self.refresh = create_refresh_token(self.user)
        self.access = create_access_token(self.user)

    def test_ok(self):
        user_data = {
            'password': 'superpass',
            'username': 'test',
        }
        resp_signin = self.client.post(self.signin_url, data=user_data, content_type='application/json')

        data = resp_signin.json()
        refresh_token = {'refresh': data['refresh']}

        resp = self.client.post(self.refresh_url, data=refresh_token, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertIn('access', data)
        self.assertIn('refresh', data)

    def test_wrong_token(self):
        refresh_token = {'refresh': 'zaluplka'}
        resp = self.client.post(self.refresh_url, data=refresh_token, content_type='application/json')
        self.assertEqual(resp.status_code, 401)

        data = resp.json()
        self.assertEqual(data['errors'][0]['jwt'], 'Token decode error')

    def test_bad_token(self):
        refresh_token = {
            'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjU5MDI5NDIuMzIxNjU3LCJpYXQiOjE3MjMzMTA5NDIuMzIxNjU3LCJqdGkiOiJkMzI4N2JhNS03YWE2LTRmMzQtOWZiNC1hZGEzNGIzZWZkMWIiLCJ1c2VyX2lkIjoxLCJ0eXBlIjoicmVmcmVzaCJ9.u_JLiXcmbSWBiy7X64M9Sb0mqCZDH82_p4j5UgU7wEE'}  # noqa: E501
        resp = self.client.post(self.refresh_url, data=refresh_token, content_type='application/json')
        self.assertEqual(resp.status_code, 401)

        data = resp.json()
        self.assertEqual(data['errors'][0]['jwt'], 'Token decode error')

    def test_miss_user_id_payload(self):
        refresh_token = {
            'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjU5MDI5NDIuMzIxNjU3LCJpYXQiOjE3MjMzMTA5NDIuMzIxNjU3LCJqdGkiOiJkMzI4N2JhNS03YWE2LTRmMzQtOWZiNC1hZGEzNGIzZWZkMWIiLCJ0eXBlIjoicmVmcmVzaCJ9.WdQdAV1hcGKX6PhE3PJIIZB4BlSOZLawxs6gBMZQInw'}  # noqa: E501
        resp = self.client.post(self.refresh_url, data=refresh_token, content_type='application/json')
        self.assertEqual(resp.status_code, 401)

        data = resp.json()
        self.assertEqual(data['errors'][0]['jwt'], 'User id not found in payload')

    def test_wrong_user_id_payload(self):
        refresh_token = {
            'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjU5MDI5NDIuMzIxNjU3LCJpYXQiOjE3MjMzMTA5NDIuMzIxNjU3LCJqdGkiOiJkMzI4N2JhNS03YWE2LTRmMzQtOWZiNC1hZGEzNGIzZWZkMWIiLCJ1c2VyX2lkIjoyMjgsInR5cGUiOiJyZWZyZXNoIn0.m8KkJmuLeUx63qELDJKMNVPWjwH6pqaI9_kTkV0ogFE'}  # noqa: E501
        resp = self.client.post(self.refresh_url, data=refresh_token, content_type='application/json')
        self.assertEqual(resp.status_code, 401)

        data = resp.json()
        self.assertEqual(data['errors'][0]['user'], 'User dose not exist')

    def test_token_type(self):
        refresh_token = {
            'refresh': self.access,
        }
        resp = self.client.post(self.refresh_url, data=refresh_token, content_type='application/json')
        self.assertEqual(resp.status_code, 401)

        data = resp.json()
        self.assertEqual(data['errors'][0]['jwt'], 'Token type is not refresh')

    def test_revoked_token(self):
        with patch("qt_auth.api.is_token_revoked") as m_is_token_revoked:
            m_is_token_revoked.return_value = True

            refresh_token = {
                'refresh': self.refresh,
            }
            resp = self.client.post(self.refresh_url, data=refresh_token, content_type='application/json')
            self.assertEqual(resp.status_code, 401)

            data = resp.json()
            self.assertEqual(data['errors'][0]['jwt'], 'Refresh token has been revoked')
