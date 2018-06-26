from django.test import TestCase
from django.test import TransactionTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client


class ServiceTestCase(TransactionTestCase):
    def setUp(self):
        User.objects.create_user(username="user1", email="user1@test.com", password="12345678")
        User.objects.create_user(username="user2", email="user2@test.com", password="12345678")
        self.client = Client()

    def test_jwt_auth(self):
        user1 = User.objects.get(username='user1')
        data = '{"username": "' + user1.username + '", "password": "' + user1.password + '"}'

        response = self.client.post(
            reverse('token_obtain_pair'),
            data=data,
            content_type='application/json',
        )
        self.assertEqual(200, response.status_code)
        self.assertContains(response.context, 'access')

