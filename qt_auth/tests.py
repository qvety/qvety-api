from django.test import TestCase

from qt_user.models import User


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
