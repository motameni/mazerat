from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User as BaseUser
from .models import *


class UserInline(admin.StackedInline):
    model = User
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserInline, )

# Register your models here.
admin.site.unregister(BaseUser)
admin.site.register(BaseUser, UserAdmin)
admin.site.register(InstagramAccount)
admin.site.register(InstagramFavoriteAccount)
admin.site.register(InstagramFollowedAccount)
admin.site.register(InstagramTag)

