from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "grade", "body", "created_at")


admin.site.register(Post, PostAdmin)
