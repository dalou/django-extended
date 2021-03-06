import os
from django.conf import settings
from django.contrib.staticfiles import finders

EXTENDED_TINYMCE_URL = getattr(settings, 'EXTENDED_TINYMCE_URL', "//tinymce.cachefly.net/4.3/tinymce.min.js")

EXTENDED_TINYMCE_DEFAULT_CONFIG = getattr(settings, 'EXTENDED_TINYMCE_DEFAULT_CONFIG',
    {
        # 'theme': "simple",
        'relative_urls': False
    }
)