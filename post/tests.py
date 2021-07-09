from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.test import APITestCase

from user.models import User
from .models import Post


class PostTests(APITestCase):
    def setUp(self) -> None:
        url = "/auth/registration/"
        data = {
            "email": "test@test.com",
            "username": "tester",
            "password": "rootroot",
        }
        Post.objects.create(id=1, user_id=1, grade=5, body="Good", created_at=parse_date("2021-07-07"))

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "test@test.com")

        self.jwt_token = response.headers["Token"]

    def test_create_post(self):
        url = "/posts/"
        data = {"grade": "5", "body": "Good"}

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.jwt_token}")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.get(id=2).body, "Good")

    def test_get_post_unauthorized(self):
        response = self.client.get("/posts/1/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.jwt_token}")
        response = self.client.get("/posts/1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), 1)
        self.assertEqual(response.data.get("grade"), 5)
        self.assertEqual(response.data.get("body"), "Good")

    def test_get_my_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.jwt_token}")
        response = self.client.get("/posts/my/?year=2021&month=7")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get("id"), 1)
        self.assertEqual(response.data[0].get("grade"), 5)
        self.assertEqual(response.data[0].get("body"), "Good")

    def test_get_shared_posts_none(self):
        response = self.client.get("/posts/share/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_shared_posts_yes(self):
        Post.objects.filter(id=1).update(share=True)

        response = self.client.get("/posts/share/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_patch_post(self):
        data = {"grade": 4, "body": "Nice"}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.jwt_token}")
        response = self.client.patch("/posts/1/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), 1)
        self.assertEqual(response.data.get("grade"), 4)
        self.assertEqual(response.data.get("body"), "Nice")

    def test_delete_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.jwt_token}")
        response = self.client.delete("/posts/1/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
