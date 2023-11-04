from django.db.models import Count
from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    amount_of_likes = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ("id", "user", "title", "description", "image", "date_posted", "amount_of_likes")
        read_only_fields = ("id", "date_posted", "amount_of_likes", "user")

    @staticmethod
    def get_amount_of_likes(instance) -> int:
        annotated_queryset = Post.objects.annotate(likes_count=Count("likes"))
        post = annotated_queryset.get(id=instance.id)
        return post.likes_count
