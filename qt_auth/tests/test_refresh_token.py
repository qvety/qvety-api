from unittest.mock import patch

from django.test import TestCase

from qt_auth.logic.services.jwt_service import JWTService
from qt_auth.tests.factories import UserFactory


class RefreshTokenTestCase(TestCase):
    def setUp(self):
        self.signin_url = '/api/auth/signin'
        self.refresh_url = '/api/auth/refresh'
        self.base_user_data = {
            'password': 'superpass',
            'username': 'test',
            'email': 'test@test.com',
        }
        self.user = UserFactory()

        jwt_service = JWTService(self.user)
        self.refresh = jwt_service.create_refresh_token()
        self.access = jwt_service.create_access_token()

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
        self.assertEqual(data['detail'], 'JWT token decode error')

    def test_bad_token(self):
        refresh_token = {
            'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjU5MDI5NDIuMzIxNjU3LCJpYXQiOjE3MjMzMTA5NDIuMzIxNjU3LCJqdGkiOiJkMzI4N2JhNS03YWE2LTRmMzQtOWZiNC1hZGEzNGIzZWZkMWIiLCJ1c2VyX2lkIjoxLCJ0eXBlIjoicmVmcmVzaCJ9.u_JLiXcmbSWBiy7X64M9Sb0mqCZDH82_p4j5UgU7wEE'}  # noqa: E501
        resp = self.client.post(self.refresh_url, data=refresh_token, content_type='application/json')
        self.assertEqual(resp.status_code, 401)

        data = resp.json()
        self.assertEqual(data['detail'], 'JWT token decode error')

    def test_miss_user_id_payload(self):
        refresh_token = {
            'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjU5MDI5NDIuMzIxNjU3LCJpYXQiOjE3MjMzMTA5NDIuMzIxNjU3LCJqdGkiOiJkMzI4N2JhNS03YWE2LTRmMzQtOWZiNC1hZGEzNGIzZWZkMWIiLCJ0eXBlIjoicmVmcmVzaCJ9.WdQdAV1hcGKX6PhE3PJIIZB4BlSOZLawxs6gBMZQInw'}  # noqa: E501
        resp = self.client.post(self.refresh_url, data=refresh_token, content_type='application/json')
        self.assertEqual(resp.status_code, 401)

        data = resp.json()
        self.assertEqual(data['detail'], 'Invalid payload')

    def test_wrong_user_id_payload(self):
        refresh_token = {
            'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjU5MDI5NDIuMzIxNjU3LCJpYXQiOjE3MjMzMTA5NDIuMzIxNjU3LCJqdGkiOiJkMzI4N2JhNS03YWE2LTRmMzQtOWZiNC1hZGEzNGIzZWZkMWIiLCJ1c2VyX2lkIjoyMjgsInR5cGUiOiJyZWZyZXNoIn0.m8KkJmuLeUx63qELDJKMNVPWjwH6pqaI9_kTkV0ogFE'}  # noqa: E501
        resp = self.client.post(self.refresh_url, data=refresh_token, content_type='application/json')
        self.assertEqual(resp.status_code, 401)

        data = resp.json()
        self.assertEqual(data['detail'], 'User not found')

    def test_token_type(self):
        refresh_token = {
            'refresh': self.access,
        }
        resp = self.client.post(self.refresh_url, data=refresh_token, content_type='application/json')
        self.assertEqual(resp.status_code, 401)

        data = resp.json()
        self.assertEqual(data['detail'], 'Token type is not refresh')

    def test_revoked_token(self):
        with patch('qt_auth.logic.services.jwt_service.JWTService._is_token_revoked') as m_is_token_revoked:
            m_is_token_revoked.return_value = True

            refresh_token = {
                'refresh': self.refresh,
            }
            resp = self.client.post(self.refresh_url, data=refresh_token, content_type='application/json')
            self.assertEqual(resp.status_code, 401)

            data = resp.json()
            self.assertEqual(data['detail'], 'Refresh token has been revoked')
