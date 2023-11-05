from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    amount_of_likes = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "title",
            "description",
            "image",
            "date_posted",
            "amount_of_likes",
        )
        read_only_fields = ("id", "date_posted", "amount_of_likes", "user")

    @staticmethod
    def get_amount_of_likes(instance) -> int:
        likes = instance.likes.all()
        return likes.count()

    def create(self, validated_data) -> Post:
        validated_data["user"] = self.context["request"].user
        return Post.objects.create(**validated_data)


class PostLikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = set()
