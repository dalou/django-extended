# encoding: utf-8

default_app_config = 'apps.blog.DefaultConfig'

from django.apps import AppConfig

class DefaultConfig(AppConfig):

    name = 'apps.blog'
    verbose_name = u'Blog'

    def ready(self):

        from . import models
        # from . import listeners