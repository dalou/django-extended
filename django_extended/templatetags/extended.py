# encoding: utf-8

import json
import datetime
import re
import bleach

from django import template
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.encoding import force_unicode
from django.utils.timezone import now as django_now
from django.utils.translation import to_locale, get_language
from django.template.defaultfilters import floatformat
from django.forms.utils import flatatt
from django.http import QueryDict

from classytags.core import Tag, Options
from classytags.arguments import MultiKeywordArgument, MultiValueArgument

from babel import Locale
from babel.numbers import format_number, format_decimal, format_percent

register = template.Library()


DEFAULT_CURRENCY = 'EUR'
# Send in data way to assets/js/input_format.js
CURRENCY_PATTERNS = {
    'EUR': { 'format': u'%s €', 'locale': 'fr_FR', 'spacing': ' ', 'decimal': ',', 'placeholder': 'EUR' },
    'USD': { 'format': u'$%s', 'locale': 'en_US', 'spacing': ',', 'decimal': '.', 'placeholder': 'USD' },
}

def price_format_decimal_to_currency(value, currency='EUR'):
    if value:
        try:
            if currency in CURRENCY_PATTERNS.keys():
                value = CURRENCY_PATTERNS[currency]['format'] % format_number(value, locale = CURRENCY_PATTERNS[currency]['locale'])
            else:
                return value
        except:
            return value
    return value

def price_format_currency_to_decimal(value, currency='EUR'):
    if value == None:
        return None
    value = unicode(value)
    if value.strip() == '':
        return None

    float_value = ""
    float_lock = False
    for c in value[::-1]:
        if c.isdigit():
            float_value += c
        if not float_lock and (c == '.' or c == ','):
            float_value += '.'
            float_lock = True

    try:
        return float(float_value[::-1]);
    except:
        return None


@register.filter
def percentage(value):
    if value or value == 0:
        kwargs = {
            'locale': to_locale(get_language()),
            'format': "#,##0.00 %",
        }
        return format_percent(value, **kwargs)


@register.filter
def smartdate(value):
    if isinstance(value, datetime.datetime):
        now = django_now()
    else:
        now = datetime.date.today()

    timedelta = value - now
    format = _(u"%(delta)s %(unit)s")
    delta = abs(timedelta.days)

    if delta > 30:
        delta = int(delta / 30)
        unit = _(u"mois")
    else:
        unit = _(u"jours")

    ctx = {
        'delta': delta,
        'unit': unit,
    }

    return format % ctx

@register.filter(name='formatted_price')
def formatted_price(value, currency='EUR'):
    return price_format_decimal_to_currency(value, currency)

@register.filter(name='formatted_float')
def formatted_float(value, currency='EUR'):
    return price_format_decimal_to_currency(value, currency)





@register.filter
def classname(obj):
    return obj.__class__.__name__

@register.filter
def classname_lower(obj):
    return classname(obj).lower()





@register.filter(name='sizify')
def sizify(file):
    """
    Simple kb/mb/gb size snippet for templates:

    {{ product.file.size|sizify }}
    """
    #value = ing(value)
    try:
        value = file.size
        if value < 512000:
            value = value / 1024.0
            ext = 'kb'
        elif value < 4194304000:
            value = value / 1048576.0
            ext = 'mb'
        else:
            value = value / 1073741824.0
            ext = 'gb'
        return '%s %s' % (str(round(value, 2)), ext)
    except:
        'n/a'

@register.filter
def file_sizify(value):
    return sizify(file)


@register.filter
def sanitize(html):
    return bleach.clean(html)

@register.filter
def divideby(value, arg): return int(arg) / int(value)


@register.simple_tag
def url_active(request, pattern, classname='active'):
    if request.path.strip('/').startswith(pattern):
        return classname
    return ''


@register.filter
def jsonify(obj):
    return json.dumps(obj)



@register.filter
def truncate_filename(value, args, maxchars=20, endchars='[...]'):

    """
    usage : {{ 'very_long_filename_display_blah_blah.zip'|truncate_filename:'20,...' }}
    result : very_long_file[...].zip
    """

    arg_list = [arg.strip() for arg in args.split(',')]
    # print arg_list
    if len(arg_list) == 1:
        maxchars = int(arg_list[0])
    if len(arg_list) == 2:
        endchars = arg_list[1]

    filename_ext = value.rsplit('.', 1)
    if len(filename_ext) >= 1:
        filename = filename_ext[0]
        ext = filename_ext[1]
    else:
        filename = value
        ext = ''

    if len(filename) > maxchars:
        return filename[:maxchars] + endchars + ext
    else:
        return value


@register.filter('external_url')
def external_url(url):
    if not url.startswith('http://') or not url.startswith('https://'):
        return "http://%s" % url
    return url

@register.filter
def admin_url_action(obj, action='change'):
    info = (obj._meta.app_label, obj._meta.model_name, action)
    args = None
    if action not in ['add', 'changelist']:
        args = [obj.pk]
    return reverse("admin:%s_%s_%s" % info, args=args)


class QueryParameters(Tag):
    name = 'query'
    options = Options(
        MultiKeywordArgument('kwa'),
    )

    def render_tag(self, context, kwa):
        q = QueryDict('').copy()
        q.update(kwa)
        return q.urlencode()

register.tag(QueryParameters)


class GetParameters(Tag):

    """
    {% raw %}{% get_parameters [except_field, ] %}{% endraw %}
    """
    name = 'get_parameters'
    options = Options(
        MultiValueArgument('except_fields', required=False),
    )

    def render_tag(self, context, except_fields):
        try:
            # If there's an exception (500), default context_processors may not
            # be called.
            request = context['request']
        except KeyError:
            return context

        getvars = request.GET.copy()

        for field in except_fields:
            if field in getvars:
                del getvars[field]

        return getvars.urlencode()

register.tag(GetParameters)