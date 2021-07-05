import json

from django.test import Client, TestCase

client = Client()


class PostTest(TestCase):
    def test_create_post(self):
        data = {
            "grade": "5",
            "body": "내용입니다",
        }

        response = client.post("/posts/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
