from datetime import datetime

from django.utils import timezone
from rest_framework import status, serializers
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from posts.models import Post, Like
from posts.permissions import IsOwnerOrAdminPermission
from posts.serializers import PostSerializer, PostLikeCreateSerializer


@api_view(["GET"])
def like_analytics(request) -> Response:
    """Tell the amount of likes during mentioned range.
    If it is not specified 2 values (date_form or date_to) than the range is 1 day before now.

    Example url: .../analytics/?date_from=2020-02-02&date_to=2020-02-15
    """
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    if not date_to or not date_from:
        date_to = timezone.now()
        date_from = date_to - timezone.timedelta(days=1)
    else:
        try:
            datetime.strptime(date_from, "%Y-%m-%d")
            datetime.strptime(date_to, "%Y-%m-%d")
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if date_from > date_to:
            return Response(
                {"error": "date_from should be earlier than date_to."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    amount_of_likes = len(
        Like.objects.filter(date_liked__date__range=[date_from, date_to])
    )

    return Response({f"amount_of_likes_in_the_range": amount_of_likes})


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().prefetch_related("likes").select_related("user")
    permission_classes = (IsAuthenticated, IsOwnerOrAdminPermission)

    def get_serializer_class(self) -> serializers:
        if self.action == "like_post":
            return PostLikeCreateSerializer
        return PostSerializer

    @action(
        detail=True,
        methods=["POST"],
        url_path="like",
        url_name="like_post",
        permission_classes=[IsAuthenticated],
    )
    def like_post(self, request, pk=None) -> Response:
        """Like/Unlike the post"""

        user = request.user
        post = self.get_object()

        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            return Response(
                {"message": "You unliked the post"}, status=status.HTTP_200_OK
            )
        except Like.DoesNotExist:
            Like.objects.create(user=user, post=post)
            return Response(
                {"message": "You liked the post"}, status=status.HTTP_201_CREATED
            )
