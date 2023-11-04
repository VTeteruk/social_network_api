from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from posts.models import Post, Like
from posts.permissions import IsOwnerOrAdminPermission
from posts.serializers import PostSerializer, PostLikeCreateSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = (IsOwnerOrAdminPermission,)

    def get_serializer_class(self) -> serializers:
        if self.action == "like_post":
            return PostLikeCreateSerializer
        return PostSerializer

    @action(detail=True, methods=["POST"], url_path="like")
    def like_post(self, request, pk=None) -> Response:
        user = request.user
        post = self.get_object()

        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            return Response({"message": "You unliked the post"}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            Like.objects.create(user=user, post=post)
            return Response({"message": "You liked the post"}, status=status.HTTP_201_CREATED)
