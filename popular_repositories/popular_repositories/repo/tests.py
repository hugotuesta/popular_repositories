import json
from .constants import *
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status


class RepositoryPopularityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.no_repo_payload = {
        }
        self.popular_repo_payload = {
            'repository': 'octocat/hello-world'
        }
        self.not_popular_repo_payload = {
            'repository': 'hugotuesta/popular_repositories'
        }
        self.error_payload = {
            'repository': 'hugotuesta_/popular_repositories'
        }

    def test_no_repository_parameter(self):
        response = self.client.post(
            reverse('calculate_popularity'),
            data=json.dumps(self.no_repo_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], ENTER_REPOSITORY_MESSAGE)

    def test_popular_repository(self):
        response = self.client.post(
            reverse('calculate_popularity'),
            data=json.dumps(self.popular_repo_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], POPULAR_REPO_MESSAGE)

    def test_not_popular_repository(self):
        response = self.client.post(
            reverse('calculate_popularity'),
            data=json.dumps(self.not_popular_repo_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], NOT_POPULAR_MESSAGE)

    def test_error_calculating_popularity(self):
        response = self.client.post(
            reverse('calculate_popularity'),
            data=json.dumps(self.error_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], ERROR_MESSAGE)
