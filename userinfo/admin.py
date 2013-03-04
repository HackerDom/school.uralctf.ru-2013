# coding=utf-8
from django.contrib import admin
from .models import UserInfo


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['ulogin', 'user', 'country', 'city', 'bdate']


admin.site.register(UserInfo, UserInfoAdmin)
