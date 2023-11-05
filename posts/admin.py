from django.contrib import admin

from posts.models import Post, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "date_posted")
    list_filter = ("title", "date_posted")
    search_fields = ("title",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_filter = ("date_liked",)
