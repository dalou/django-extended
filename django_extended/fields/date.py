
# from tinymce.models import HTMLField as TinyMceHTMLField

from django.db import models
from ..forms import DateInput, DateTimeField, DateField, DateInput


class DateTimeField(models.DateTimeField):
    """
    A large string field for HTML content. It uses the TinyMCE widget in
    forms.
    """

    def formfield(self, **kwargs):
        # kwargs['form_class'] = DateTimeField
        kwargs['widget'] = DateInput

        return super(DateTimeField, self).formfield(**kwargs)


class DateField(models.DateField):


    def formfield(self, **kwargs):
        kwargs['form_class'] = DateField
        # kwargs['widget'] = DateInput

        return super(DateField, self).formfield(**kwargs)

# try:
#     from south.modelsinspector import add_introspection_rules
#     add_introspection_rules([], ["^django_extended\.fields\.HtmlField"])
# except ImportError:
#     pass