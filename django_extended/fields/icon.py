# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.utils.text import capfirst

from ..forms import IconField as IconFormField, IconInput


class IconField(models.CharField):
    """
    A text field made to accept hexadecimal color value (#FFFFFF)
    with a color picker widget.
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        super(IconField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = IconInput
        return super(IconField, self).formfield(**kwargs)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_extended\.fields\.IconField"])
except ImportError:
    pass