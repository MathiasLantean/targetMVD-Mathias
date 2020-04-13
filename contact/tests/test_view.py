from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker
from contact.tests.factories import InformationFactory
from profile.tests.factories import CommonUserFactory


class TargetTests(APITestCase):

    def test_get_about_info(self):
        url = reverse('info-detail', kwargs={'pk': 'about'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_generic_section_info(self):
        info = InformationFactory()
        url = reverse('info-detail', kwargs={'pk': info.title})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_existing_section_info(self):
        url = reverse('info-detail', kwargs={'pk': 'info_does_not_exist'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SendQuestionTests(APITestCase):

    def setUp(self):
        self.test_active_user = CommonUserFactory()

    def test_send_question_ok(self):
        self.client.force_login(self.test_active_user)
        url = reverse("send_question")
        data = {
            "question": Faker().paragraph(nb_sentences=10),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_send_question_empty(self):
        self.client.force_login(self.test_active_user)
        url = reverse("send_question")
        data = {
            "question": '',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_question_wrong_payload(self):
        self.client.force_login(self.test_active_user)
        url = reverse("send_question")
        data = {
            "wrong": Faker().paragraph(nb_sentences=10),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_question_no_logged_user(self):
        url = reverse("send_question")
        data = {
            "question": Faker().paragraph(nb_sentences=10),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
