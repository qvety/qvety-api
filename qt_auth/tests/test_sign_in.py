from datetime import datetime

from django.test import TestCase

from qt_auth.logic.services.jwt_service import JWTService
from qt_auth.tests.factories import UserFactory


class SignInTestCase(TestCase):
    def setUp(self):
        self.signin_url = '/api/auth/signin'
        self.base_user_data = {
            'password': 'superpass',
            'username': 'test',
            'email': 'test@test.com',
        }
        self.user = UserFactory()

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
        self.assertEqual(resp.status_code, 401)

        data = resp.json()
        self.assertEqual(data['detail'], 'Invalid credentials')

    def test_wrong_password(self):
        user_data = {
            'password': 'zalupka228',
            'username': 'test',
        }
        resp = self.client.post(self.signin_url, data=user_data, content_type='application/json')
        self.assertEqual(resp.status_code, 401)

        data = resp.json()
        self.assertEqual(data['detail'], 'Invalid credentials')

    def test_token_data(self):
        user_data = {
            'password': 'superpass',
            'username': 'test',
        }
        resp = self.client.post(self.signin_url, data=user_data, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        access, refresh = data['access'], data['refresh']
        jwt_service = JWTService()
        verified_payload_access = jwt_service._get_verify_payload_from_unverified_token(access, 'access')
        verified_payload_refresh = jwt_service._get_verify_payload_from_unverified_token(refresh, 'refresh')
        fifteen_minutes_timestamp = datetime.now().timestamp() + 60 * 15
        one_day_timestamp = datetime.now().timestamp() + 30 * 24 * 60 * 60

        self.assertLess(verified_payload_access['exp'], fifteen_minutes_timestamp)
        self.assertEqual(verified_payload_access['user_id'], self.user.id)
        self.assertEqual(verified_payload_access['type'], 'access')

        self.assertLess(verified_payload_refresh['exp'], one_day_timestamp)
        self.assertLess(fifteen_minutes_timestamp, verified_payload_refresh['exp'])
        self.assertEqual(verified_payload_refresh['user_id'], self.user.id)
        self.assertEqual(verified_payload_refresh['type'], 'refresh')
