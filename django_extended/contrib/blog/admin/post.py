# encoding: utf-8

from django import forms
from django.conf import settings
from django.contrib import admin

from ..models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'published_date', 'owner')
    pass

admin.site.register(Post, PostAdmin)