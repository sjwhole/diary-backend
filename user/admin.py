from django.contrib import admin
from django.contrib.auth.models import Group

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'nickname',
        'date_joined',
    )

    list_display_links = (
        'username',
    )


admin.site.unregister(Group)
