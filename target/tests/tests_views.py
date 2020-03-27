from django.contrib.gis.geos import Point
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from profile.models import User
from ..models import Target


class TargetTests(TestCase):

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
        self.test_target_uno = Target.objects.create(
            user=self.test_superuser,
            title='target test',
            radius=45000.02,
            location=Point(-56.164532, -34.901112)
        )
        self.test_target_dos = Target.objects.create(
            user=self.test_active_user,
            title='target test',
            radius=5000.99,
            location=Point(-54.100002, -33.900002)
        )

    def test_get_map_page_ok(self):
        url = reverse('target_map')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_target_as_not_logged_user(self):
        url = reverse("target-list")
        data = {
            "title": "Point",
            "radius": 45000,
            "location": "POINT (-42.796763 -5.077056)"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_target(self):
        self.client.force_login(self.test_active_user)
        url = reverse("target-list")
        data = {
            "title": "Point",
            "radius": 45000,
            "location": "POINT (-42.796763 -5.077056)"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('properties').get('user'), self.test_active_user.id)

    def test_get_target_list_as_superuser(self):
        self.client.force_login(self.test_superuser)
        url = reverse("target-list")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('features')), Target.objects.all().count())

    def test_get_target_list_as_user(self):
        self.client.force_login(self.test_active_user)
        url = reverse("target-list")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('features')), Target.objects.filter(user=self.test_active_user).count())
