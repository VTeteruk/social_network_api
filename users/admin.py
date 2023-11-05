from django.contrib import admin
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "last_login")
    search_fields = ("username",)
