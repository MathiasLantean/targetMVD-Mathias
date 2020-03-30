import base64

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from ..models import User


class UserAuthTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_email = 'test@test.com'
        cls.user_password = 'test123455'

    def setUp(self):
        self.test_superuser = User.objects.create_user(
            email='defaultadmin@defaultadmin.com',
            password=self.user_password,
            gender=1,
            is_superuser=True
        )
        self.test_active_user = User.objects.create_user(
            email='default@default.com',
            password=self.user_password,
            gender=3
        )
        self.test_inactive_user = User.objects.create_user(
            email='defaultinactive@default.com',
            password=self.user_password,
            gender=3,
            is_active=False,
        )
        token_generator = PasswordResetTokenGenerator()
        self.token = token_generator.make_token(self.test_active_user)
        self.uid = (base64.b64encode(str(self.test_active_user.id).encode('ascii'))).decode("utf-8")

    def test_sign_up_user_ok(self):
        url = reverse("auth:rest_register")
        data = {
            'email': self.user_email,
            'gender': User.Gender.GENDER_MALE,
            'password1': self.user_password,
            'password2': self.user_password,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get('key'))

    def test_sign_up_user_wrong_password(self):
        url = reverse("auth:rest_register")
        data = {
            'email': self.user_email,
            'gender': User.Gender.GENDER_MALE,
            'password1': '',
            'password2': ''
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_user_password_doesnt_match(self):
        url = reverse("auth:rest_register")
        data = {
            'email': self.user_email,
            'gender': User.Gender.GENDER_MALE,
            'password1': self.user_password,
            'password2': 'test1234556'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_user_duplicate_email(self):
        url = reverse("auth:rest_register")
        data = {
            'email': self.test_active_user.email,
            'gender': User.Gender.GENDER_MALE,
            'password1': self.user_password,
            'password2': self.user_password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_log_in_ok(self):
        url = reverse("rest_login")
        data = {
            'email': self.test_active_user.email,
            'password': self.user_password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('key'))

    def test_log_in_wrong(self):
        url = reverse("rest_login")
        data = {
            'email': self.test_active_user.email,
            'password': ''
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_log_in_inactive_user(self):
        url = reverse("rest_login")
        data = {
            'email': self.test_inactive_user.email,
            'password': self.user_password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_log_out_ok(self):
        url_login = reverse("rest_login")
        data_login = {
            'email': self.test_active_user.email,
            'password': self.user_password
        }
        response_login = self.client.post(url_login, data_login, format='json')
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
        key = response_login.data.get('key')
        url_logout = reverse("rest_logout")
        data_logout = {
            'key': key
        }
        response_logout = self.client.post(url_logout, data_logout, format='json')
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)

    def test_get_facebook_token_page_ok(self):
        url = reverse('fb_token')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_reset_password_email_ok(self):
        url = reverse("rest_password_reset")
        data = {
            'email': self.test_active_user.email
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_reset_password_email_wrong_email(self):
        url = reverse("rest_password_reset")
        data = {
            'email': 'wrong_email@wrong'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_reset_page_ok(self):
        url = reverse('account_reset_password_from_key', kwargs={'uidb64': self.uid[:2], 'token': self.token})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_ok(self):
        url = reverse('rest_password_reset_confirm')
        data = {
            "new_password1": "newPassForDefault",
            "new_password2": "newPassForDefault",
            "uid": self.uid,
            "token": self.token,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_wrong_password_format(self):
        url = reverse('rest_password_reset_confirm')
        data = {
            "new_password1": "test",
            "new_password2": "test",
            "uid": self.uid,
            "token": self.token,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password_does_not_match(self):
        url = reverse('rest_password_reset_confirm')
        data = {
            "new_password1": "test",
            "new_password2": "test123",
            "uid": self.uid,
            "token": self.token,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_list_as_admin(self):
        self.client.force_login(self.test_superuser)
        url = reverse('user_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), User.objects.all().count())

    def test_get_user_list_as_common_user(self):
        self.client.force_login(self.test_active_user)
        url = reverse('user_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_list_as_not_logged_user(self):
        url = reverse('user_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
