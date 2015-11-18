# encoding: utf-8

default_app_config = 'apps.emailing.DefaultConfig'

from django.apps import AppConfig

class DefaultConfig(AppConfig):

    name = 'apps.emailing'
    verbose_name = u'Emailing'

    def ready(self):

        from . import models
