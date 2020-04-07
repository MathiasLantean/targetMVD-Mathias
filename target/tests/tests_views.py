import io
from PIL import Image

from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

from target.models import Target, Topic
from profile.tests.factories import AdminUserFactory, CommonUserFactory
from target.tests.factories import TargetFactory, TopicFactory


class TargetTests(TestCase):

    def setUp(self):
        self.test_superuser = AdminUserFactory()
        self.test_active_user = CommonUserFactory()
        self.test_target_uno = TargetFactory(
            user=self.test_superuser,
        )
        self.test_target_dos = TargetFactory(
            user=self.test_active_user,
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

    def test_create_more_targets_than_it_is_allowed(self):
        initial_num_of_targets = self.test_active_user.target_set.count()
        for i in range(0, (settings.MAX_NUMBER_OF_TARGETS - initial_num_of_targets)):
            TargetFactory(user=self.test_active_user)

        self.client.force_login(self.test_active_user)
        url = reverse("target-list")
        data = {
            "title": "Point",
            "radius": 45000,
            "location": "POINT (-42.796763 -5.077056)"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertLessEqual(self.test_active_user.target_set.count(), settings.MAX_NUMBER_OF_TARGETS)

    def test_get_target_list_as_admin(self):
        self.client.force_login(self.test_superuser)
        url = reverse("target-list")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('features')), Target.objects.all().count())

    def test_get_target_list_as_common_user(self):
        self.client.force_login(self.test_active_user)
        url = reverse("target-list")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('features')), Target.objects.filter(user=self.test_active_user).count())

    def test_delete_target_ok(self):
        self.client.force_login(self.test_active_user)
        target_to_delete = TargetFactory(user=self.test_active_user)
        url = reverse("target-detail", kwargs={'pk': target_to_delete.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_target_of_another_user_as_common_user(self):
        self.client.force_login(self.test_active_user)
        target_to_delete = TargetFactory()
        url = reverse("target-detail", kwargs={'pk': target_to_delete.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_target_of_another_user_as_admin(self):
        self.client.force_login(self.test_superuser)
        target_to_delete = TargetFactory()
        url = reverse("target-detail", kwargs={'pk': target_to_delete.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TopicTests(APITestCase):

    def setUp(self):
        self.test_superuser = AdminUserFactory()
        self.test_active_user = CommonUserFactory()
        self.test_topic = TopicFactory()

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
