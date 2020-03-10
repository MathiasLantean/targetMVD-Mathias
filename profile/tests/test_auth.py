from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import User


class UserAuthTests(APITestCase):
    def setUp(self):
        test_active_user = User.objects.create_user(email='default@default.com', password='hello123455', gender=3)
        test_inactive_user = User.objects.create_user(email='default2@default2.com',
                                                      password='hello123455',
                                                      gender=3,
                                                      is_active=False)

    def test_sign_up_user_ok(self):
        url = reverse("auth:rest_register")
        data = {'email': 'test@test.com',
                'gender': User.Gender.GENDER_MALE,
                'password1': 'test123455',
                'password2': 'test123455'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get('detail'))

    def test_sign_up_user_wrong_password(self):
        url = reverse("auth:rest_register")
        data = {'email': 'test@test.com',
                'gender': User.Gender.GENDER_MALE,
                'password1': '',
                'password2': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_user_password_doesnt_match(self):
        url = reverse("auth:rest_register")
        data = {'email': 'test@test.com',
                'gender': User.Gender.GENDER_MALE,
                'password1': 'test1234556',
                'password2': 'test123455'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_user_duplicate_email(self):
        url = reverse("auth:rest_register")
        data = {'email': 'default@default.com',
                'gender': User.Gender.GENDER_MALE,
                'password1': 'test123455',
                'password2': 'test123455'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_log_in_ok(self):
        url = reverse("rest_login")
        data = {'email': 'default@default.com',
                'password': 'hello123455'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('key'))

    def test_log_in_wrong(self):
        url = reverse("rest_login")
        data = {'email': 'default@default.com',
                'password': 'hello123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_log_in_inactive_user(self):
        url = reverse("rest_login")
        data = {'email': 'default2@default2.com',
                'password': 'hello123455'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_log_out_ok(self):
        url_login = reverse("rest_login")
        data_login = {'email': 'default@default.com', 'password': 'hello123455'}
        response_login = self.client.post(url_login, data_login, format='json')
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
        key = response_login.data.get('key')
        url_logout = reverse("rest_logout")
        data_logout = {'key': key}
        response_logout = self.client.post(url_logout, data_logout, format='json')
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)
