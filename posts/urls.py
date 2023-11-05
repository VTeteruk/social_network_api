from django.urls import path
from rest_framework import routers
from posts.views import PostViewSet, like_analytics

router = routers.DefaultRouter()
router.register("", PostViewSet)

urlpatterns = [
    path("analytics/", like_analytics, name="like-analytics"),
] + router.urls

app_name = "posts"
