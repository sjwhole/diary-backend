from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Post


class PostTests(APITestCase):
    def test_create_post(self):
        url = reverse("post-list")
        data = {"grade": "5", "body": "Good"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().body, "Good")

    def test_get_post(self):
        Post.objects.create(id=1, grade=5, body="Good")

        response = self.client.get("/posts/1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), 1)
        self.assertEqual(response.data.get("grade"), 5)
        self.assertEqual(response.data.get("body"), "Good")

    def test_patch_post(self):
        Post.objects.create(id=1, grade=5, body="Good")

        data = {"grade": 4, "body": "Nice"}
        response = self.client.patch("/posts/1/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), 1)
        self.assertEqual(response.data.get("grade"), 4)
        self.assertEqual(response.data.get("body"), "Nice")

    def test_delete_post(self):
        Post.objects.create(id=1, grade=5, body="Good")

        response = self.client.delete("/posts/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
