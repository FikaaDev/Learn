from rest_framework.test import APITestCase, APIRequestFactory
from .views import PostListCreateView
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model


User = get_user_model()


class HelloWorldTestCase(APITestCase):
    def test_hello_world(self):
        response = self.client.get(reverse("posts_home"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Message"], "Hello")


class PostListCreateTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("class_based_list_posts_generics")

    def authenticate(self):
        self.client.post(
            reverse("signup"),
            {
                "email": "jonathan@app.com",
                "password": "password##!123",
                "username": "jonathan",
            },
        )

        response = self.client.post(
            reverse("login"),
            {
                "email": "jonathan@app.com",
                "password": "password##!123",
            },
        )

        print(response.data)

        token = response.data["tokens"]["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_post_creation(self):
        self.authenticate()

        sample_data = {"title": "Sample title", "content": "Sample content"}
        response = self.client.post(reverse("class_based_list_posts_generics"), sample_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], sample_data["title"])