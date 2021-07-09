from django.contrib import admin
from django.contrib.auth.models import Group

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'date_joined',
    )

    list_display_links = (
        'username',
        'email',
    )


admin.site.unregister(Group)
