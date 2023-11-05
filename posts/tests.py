from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from posts.models import Post, Like


class PostAPITest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(
            title="Test Post",
            description="This is a test post",
            user=self.user,
        )

    def test_create_post(self) -> None:
        url = reverse("posts:post-list")
        data = {
            "title": "New Post",
            "description": "A new post description",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_like_post(self) -> None:
        url = reverse("posts:post-like_post", kwargs={"pk": self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

    def test_unlike_post(self) -> None:
        Like.objects.create(user=self.user, post=self.post)
        url = reverse("posts:post-like_post", kwargs={"pk": self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 0)

    def test_like_analytics(self) -> None:
        Like.objects.create(user=self.user, post=self.post)
        Like.objects.create(user=self.user, post=self.post)
        url = reverse("posts:like-analytics")
        response = self.client.get(
            url, data={"date_from": "2000-01-01", "date_to": "2000-01-01"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount_of_likes_in_the_range"], 0)

        response = self.client.get(url)
        self.assertEqual(response.data["amount_of_likes_in_the_range"], 2)


class UnauthorizedUserAPITest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_unauthorized_create_post(self) -> None:
        url = reverse("posts:post-list")
        data = {
            "title": "New Post",
            "description": "A new post description",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_like_post(self) -> None:
        url = reverse(
            "posts:post-like_post", kwargs={"pk": 1}
        )  # Replace 1 with a valid post ID
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_unlike_post(self) -> None:
        url = reverse(
            "posts:post-like_post", kwargs={"pk": 1}
        )  # Replace 1 with a valid post ID
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_like_analytics(self) -> None:
        url = reverse("posts:like-analytics")
        response = self.client.get(
            url, data={"date_from": "2000-01-01", "date_to": "2000-01-01"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class IsOwnerOrAdminPermissionTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin_user", password="admin_password"
        )
        self.post = Post.objects.create(
            title="Test Post",
            description="This is a test post",
            user=self.user,
        )

    def test_owner_has_permission(self) -> None:
        url = reverse("posts:post-detail", kwargs={"pk": self.post.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_has_permission(self) -> None:
        url = reverse("posts:post-detail", kwargs={"pk": self.post.id})
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_users_do_not_have_permission(self) -> None:
        other_user = get_user_model().objects.create_user(
            username="other_user", password="other_password"
        )
        url = reverse("posts:post-detail", kwargs={"pk": self.post.id})
        self.client.force_authenticate(user=other_user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthenticated_users_do_not_have_permission(self) -> None:
        url = reverse("posts:post-detail", kwargs={"pk": self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
