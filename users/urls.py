from django.urls import path

from users.views import UserDetailView, CreateUserView, show_activity

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("me/", UserDetailView.as_view(), name="user-details"),
    path("me/activity/", show_activity, name="user-activity")
]

app_name = "users"
