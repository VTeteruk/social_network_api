from rest_framework.viewsets import ModelViewSet

from posts.models import Post
from posts.permissions import IsOwnerOrAdminPermission
from posts.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrAdminPermission,)
