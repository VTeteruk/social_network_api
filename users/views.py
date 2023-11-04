from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Show information about current user"""

    serializer_class = UserSerializer

    def get_object(self) -> User:
        return get_user_model().objects.get(id=self.request.user.id)


@api_view(["GET"])
def show_activity(request) -> Response:
    user = request.user
    return Response(
        {"last_login": user.last_login, "last_time_request": user.last_time_request},
        status=status.HTTP_200_OK
    )
