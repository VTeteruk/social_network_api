from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


class UserTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user", email="test_user@example.com", password="test_password"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_user(self) -> None:
        url = reverse("users:register")
        data = {
            "username": "new_user",
            "email": "new_user@example.com",
            "password": "new_password",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_get_user_details(self) -> None:
        url = reverse("users:user-details")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_details(self) -> None:
        url = reverse("users:user-details")
        data = {"first_name": "New", "last_name": "Name", "password": "test_password"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "New")
        self.assertEqual(self.user.last_name, "Name")

    def test_user_activity(self) -> None:
        url = reverse("users:user-activity")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_activity(self) -> None:
        client = APIClient()
        url = reverse("users:user-activity")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MiddlewareTests(TestCase):
    def test_update_last_request_middleware(self) -> None:
        user = get_user_model().objects.create_user(
            username="test_user", email="testuser@example.com", password="test_password"
        )
        client = APIClient()
        login_url = reverse("users:token_obtain_pair")
        response = client.post(
            login_url, data={"username": "test_user", "password": "test_password"}
        )
        token = response.data["access"]

        headers = {"Authorization": f"Bearer {token}"}

        # Simulate a request to trigger the middleware
        url = reverse("users:user-activity")
        client.get(url, headers=headers)

        user.refresh_from_db()
        self.assertIsNotNone(user.last_time_request)
        self.assertIsNotNone(user.last_login)

    def test_invalid_token_middleware(self) -> None:
        client = APIClient()
        url = reverse("users:user-activity")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
