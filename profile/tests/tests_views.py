from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json
from ..models import User


class UserTests(APITestCase):
    def setUp(self):
        self.user_one = User.objects.create_user(email="userone@userone.com",
                                                 password="userone1234",
                                                 gender=User.Gender.GENDER_FEMALE)

    def test_create_user_ok(self):
        url = reverse("app-profile:users-list")
        data = {'email': 'test@test.com', 'gender': User.Gender.GENDER_MALE, 'password': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get('pk'))
        self.assertEqual(response.data.get('gender'), User.Gender.GENDER_MALE)

    def test_create_user_empty_email(self):
        url = reverse("app-profile:users-list")
        data = {'email': '', 'gender': User.Gender.GENDER_MALE, 'password': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_wrong_email(self):
        url = reverse("app-profile:users-list")
        data = {'email': 'test@test', 'gender': User.Gender.GENDER_MALE, 'password': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_empty_gender(self):
        url = reverse("app-profile:users-list")
        data = {'email': '', 'gender': '', 'password': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_wrong_gender(self):
        url = reverse("app-profile:users-list")
        data = {'email': '', 'gender': 9, 'password': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_user_ok(self):
        url = reverse("app-profile:users-detail", kwargs={'pk': self.user_one.pk})
        data = {'email': 'test@test.com', 'gender': User.Gender.GENDER_MALE, 'password': 'test'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user_one.pk, response.data.get('pk'))
        self.assertEqual(response.data.get('gender'), User.Gender.GENDER_MALE)

    def test_edit_user_empty_email(self):
        url = reverse("app-profile:users-detail", kwargs={'pk': self.user_one.pk})
        data = {'email': '', 'gender': User.Gender.GENDER_MALE, 'password': 'test'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_user_empty_email(self):
        url = reverse("app-profile:users-detail", kwargs={'pk': self.user_one.pk})
        data = {'email': 'test.test', 'gender': User.Gender.GENDER_MALE}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
