import io
from PIL import Image

from django.contrib.gis.geos import Point
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profile.models import User
from ..models import Target, Topic


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

    def test_get_map_page_user_not_logged(self):
        url = reverse('target_map')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_get_map_page_ok(self):
        self.client.force_login(self.test_active_user)
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


class TopicTests(APITestCase):

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
        self.test_topic = Topic.objects.create(
            title='Test'
        )

    @classmethod
    def generate_photo_file(cls):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_create_topic_as_common_user(self):
        self.client.force_login(self.test_active_user)
        url = reverse("topic-list")
        data = {
            "title": "Bad Topic",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_topic_as_admin(self):
        self.client.force_login(self.test_superuser)
        url = reverse("topic-list")
        photo_file = self.generate_photo_file()
        data = {
            "title": "Great Topic",
            "photo": photo_file
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_topic_as_common_user(self):
        self.client.force_login(self.test_active_user)
        url = reverse("topic-list")
        data = {
            "title": "Point",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_topic_as_admin(self):
        self.client.force_login(self.test_superuser)
        url = reverse("topic-detail", kwargs={'pk': self.test_topic.id})
        photo_file = self.generate_photo_file()
        data = {
            "title": "Great Topic Edited",
            "photo": photo_file,
        }
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_topic_as_common_user(self):
        self.client.force_login(self.test_active_user)
        url = reverse("topic-list")
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_topic_as_admin(self):
        self.client.force_login(self.test_superuser)
        url = reverse("topic-detail", kwargs={'pk': self.test_topic.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_topic_list_as_admin(self):
        self.client.force_login(self.test_superuser)
        url = reverse('topic-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Topic.objects.all().count())

    def test_get_topic_list_as_common_user(self):
        self.client.force_login(self.test_active_user)
        url = reverse('topic-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Topic.objects.all().count())
