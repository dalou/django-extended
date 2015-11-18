
# encoding: utf-8

import datetime
import operator
import hashlib
import random
from email.utils import parseaddr
import functools
try:
    from urllib.parse import urlparse, urlunparse
except ImportError:  # python 2
    from urlparse import urlparse, urlunparse

from django.db import models
from django.db.models import Q
from django.contrib import auth, messages
from django.utils.translation import ugettext_lazy as _, ugettext
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model

from .models import *

def is_valid_email(email):
    result = parseaddr(email.strip())
    if '@' in result[1]:
        return result[1]
    else:
        return None


class HtmlTemplateEmail(EmailMultiAlternatives):

    def __init__(self, subject, html, sender, receivers, context={}, **kwargs):
        if type(receivers) == type(str()) or type(receivers) == type(unicode()):
            receivers = [receivers]

        text_template = strip_tags(html)
        super(HtmlTemplateEmail, self).__init__(subject, text_template, sender, receivers, **kwargs)
        self.attach_alternative(html, "text/html")


def send_html_email(subject, sender, receivers, html='', context={}, **kwargs):
    message = HtmlTemplateEmail(subject, html, sender, receivers, context, **kwargs)
    return message.send()

def send_template_email(subject, sender, receivers, template=None, context={}, **kwargs):
    html_template = get_template(template)
    context = Context(context)
    html = html_template.render(context)
    return send_html_email(subject, sender, receivers, html=html, context=context, **kwargs)


def random_token(extra=None, hash_func=hashlib.sha256):

    if extra is None:
        extra = []
    bits = extra + [str(random.SystemRandom().getrandbits(512))]
    return hash_func("".join(bits)).hexdigest()