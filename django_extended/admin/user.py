# encoding: utf-8

import datetime
import operator

from django.contrib import admin
from django.db import models

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.functional import curry

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
User = get_user_model()

class UserAdmin(BaseUserAdmin):


    class Media:
        js = ( settings.STATIC_URL + "user/js/admin.js", )

    #UserAdmin.list_display +
    list_display = (
        'email',
        'first_name',
        'last_name',
        'last_login',
        'date_joined',
        'is_active',
        'is_staff',
        'is_superuser',
    )

    list_filter = BaseUserAdmin.list_filter + (
        'is_fake',
        # 'profile__signup_source',
        # 'profile__register_from',
        # 'profile__registeration_platform'
    )
    ordering = ("-date_joined",)

    def get_queryset(self, *args, **kwargs):
        queryset = super(UserAdmin, self).get_queryset( *args, **kwargs)
        return queryset

    actions = ['' ]



    def email(self, obj):
        return obj.email
    email.short_description = "Email"


    # fieldsets = (
    #     ('Information personnelle', {
    #         'classes': ('suit-tab suit-tab-infos',),
    #         'fields': ('first_name', 'last_name', 'email') #, 'display_filters')
    #     }),
    # )

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-login',),
            'fields': ('email', 'password', 'last_login', 'date_joined')
        }),
        (_(u'Personal info'), {
            'classes': ('suit-tab suit-tab-infos',),
            'fields': ('first_name', 'last_name', 'username')
        }),
        (_(u'Permissions'), {
            'classes': ('suit-tab suit-tab-perms',),
            'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    inlines = (
        # CustomerProfileInline,
        # UserSettingsInline,
    )

    suit_form_tabs = (
        ('login', u"Login"),
        ('infos', u"Informations"),
        ('perms', u"Permissions"),
        # ('settings', u"Paramètres"),
        # ('profile', u"Profile"),
        # ('content', u"Contenus"),
    )
