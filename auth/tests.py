from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User



class AuthTests(APITestCase):
    def test_login(self):
        self.test_registration()

        url = "/auth/login/"
        data = {
            "email": "test@test.com",
            "password": "rootroot",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_registration(self):
        url = "/auth/registration/"
        data = {
            "email": "test@test.com",
            "username": "tester",
            "password": "rootroot",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "test@test.com")
