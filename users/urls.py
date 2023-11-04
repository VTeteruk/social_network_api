from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserDetailView, CreateUserView, show_activity

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("me/", UserDetailView.as_view(), name="user-details"),
    path("me/activity/", show_activity, name="user-activity"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

app_name = "users"
