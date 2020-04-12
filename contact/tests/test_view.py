from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from contact.tests.factories import InformationFactory


class TargetTests(APITestCase):

    def test_get_about_info(self):
        url = reverse('info', kwargs={'pk': 'about'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_generic_section_info(self):
        info = InformationFactory()
        url = reverse('info', kwargs={'pk': info.title})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_existing_section_info(self):
        url = reverse('info', kwargs={'pk': 'info_does_not_exists'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
