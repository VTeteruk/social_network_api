from __future__ import annotations

import os.path
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


def create_unique_file_name(instance: Post, filename: str) -> str:
    _, extension = os.path.splitext(filename)

    #  MARK: slugify returns refactored text / uuid creates a unique id
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/posts_pictures/", filename)


class Post(models.Model):
    date_posted = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(
        null=True, blank=True, upload_to=create_unique_file_name
    )
    description = models.TextField()
    user = models.ForeignKey(
        get_user_model(), related_name="posts", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"Post({self.title!r})"


class Like(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="likes", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, related_name="likes", on_delete=models.CASCADE
    )
    date_liked = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Like({self.user.first_name} liked {self.post.title})"
