from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_staff",
        )
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

    def create(self, validated_data) -> User:
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data) -> User:
        password = validated_data.pop("password")
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
