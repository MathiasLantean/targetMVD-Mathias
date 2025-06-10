from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from profile.models import User
from profile.tests.factories import CommonUserFactory, InactiveUserFactory


class UserAuthTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_email = 'test@test.com'
        cls.user_password = 'test123455'

    def setUp(self):
        self.test_active_user = CommonUserFactory(password=self.user_password)
        self.test_inactive_user = InactiveUserFactory(password=self.user_password)

    def test_sign_up_user_ok(self):
        url = reverse("auth:rest_register")
        data = {'email': self.user_email,
                'gender': User.Gender.GENDER_MALE,
                'password1': self.user_password,
                'password2': self.user_password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get('key'))

    def test_sign_up_user_wrong_password(self):
        url = reverse("auth:rest_register")
        data = {'email': self.user_email,
                'gender': User.Gender.GENDER_MALE,
                'password1': '',
                'password2': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_user_password_doesnt_match(self):
        url = reverse("auth:rest_register")
        data = {'email': self.user_email,
                'gender': User.Gender.GENDER_MALE,
                'password1': self.user_password,
                'password2': 'test1234556'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_user_duplicate_email(self):
        url = reverse("auth:rest_register")
        data = {'email': self.test_active_user.email,
                'gender': User.Gender.GENDER_MALE,
                'password1': self.user_password,
                'password2': self.user_password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_log_in_ok(self):
        url = reverse("rest_login")
        data = {'email': self.test_active_user.email,
                'password': self.user_password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('key'))

    def test_log_in_wrong(self):
        url = reverse("rest_login")
        data = {'email': self.test_active_user.email,
                'password': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_log_in_inactive_user(self):
        url = reverse("rest_login")
        data = {'email': self.test_inactive_user.email,
                'password': self.user_password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_log_out_ok(self):
        url_login = reverse("rest_login")
        data_login = {'email': self.test_active_user.email, 'password': self.user_password}
        response_login = self.client.post(url_login, data_login, format='json')
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
        key = response_login.data.get('key')
        url_logout = reverse("rest_logout")
        data_logout = {'key': key}
        response_logout = self.client.post(url_logout, data_logout, format='json')
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)
