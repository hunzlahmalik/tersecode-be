from django.urls import resolve
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ..models import User


class UserAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="test", password="test")
        self.user.save()
        self.user1 = User.objects.create(username="test1", password="test1")
        self.user1.save()
        self.user2 = User.objects.create(username="test2", password="test2")
        self.user2.save()

    def test_create_user(self):
        url = "/api/users/"
        data = {
            "username": "test",
            "password": "test",
            "email": "test@email.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)
        self.assertEqual(User.objects.get(username="test").email, "test@email.com")

    def test_get_user(self):
        url = "/api/users/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]["username"], "test")
        self.assertEqual(response.data[0]["email"], "")
        self.assertEqual(response.data[1]["username"], "test1")
        self.assertEqual(response.data[1]["email"], "")
        self.assertEqual(response.data[2]["username"], "test2")
        self.assertEqual(response.data[2]["email"], "")

    def test_get_user_by_username(self):
        url = "/api/users/test/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "test")
        self.assertEqual(response.data["email"], "")

    def test_update_user(self):
        url = "/api/users/test/"
        data = {
            "username": "test",
            "password": "test",
            "email": "updatedemail@yahoo.com",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
