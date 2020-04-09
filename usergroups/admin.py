from django.contrib import admin

from .models import UserGroup, UserGroupArticle, UserGroupComment
admin.site.register(UserGroup)
admin.site.register(UserGroupArticle)
admin.site.register(UserGroupComment)
