# encoding: utf-8

default_app_config = 'apps.flatpage.DefaultConfig'

from django.apps import AppConfig

class DefaultConfig(AppConfig):

    name = 'apps.flatpage'
    verbose_name = u'Page statique'

    def ready(self):

        from . import models