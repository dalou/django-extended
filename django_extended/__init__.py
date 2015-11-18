try:
    default_app_config = 'django_extended.DefaultConfig'

    from django.apps import AppConfig

    class DefaultConfig(AppConfig):
        name = 'django_extended'
        verbose_name = u"Django extended"

        def ready(self):

            from . import models

except:
    # Prevent from package setup
    pass
