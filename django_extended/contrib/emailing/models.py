# encoding: utf-8
import datetime
import operator
import hashlib
import urllib
import random
import re

from django.conf import settings
from django.db import models
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.sites.models import Site

from .utils import *



class UserActivationToken(models.Model):
    email = models.EmailField(u"Adresse email", max_length=254, unique=True, db_index=True)
    token = models.CharField(u"Token d'activation", max_length=64, unique=True, db_index=True)
    is_used = models.BooleanField(u'Utilisé ?', default=False)
    expiration_date = models.DateTimeField(u"date d'expiration", blank=True, null=True)

    _hash_func = hashlib.sha256

    def save(self, **kwargs):
        if not self.token:
            bits = [self.email, str(random.SystemRandom().getrandbits(512))]
            self.token =  self._hash_func("".join(bits).encode("utf-8")).hexdigest()
        super(UserActivationToken, self).save(**kwargs)

    def activate_user(self, user):
        if not user.is_active:
            user.is_active = True
            self.save()
            return True
        return False

    def get_activate_url(self):
        return "{0}://{1}{2}".format(
            getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http"),
            Site.objects.get_current(),
            reverse("emailing:activate-user", args=[self.token])
        )

    def authenticate_user(self, request, user, remember=False):
        if not hasattr(user, 'backend'):
            user.backend = 'apps.user.auth.AuthModelBackend'
        if request.user.is_authenticated():
            auth.logout(request)
        auth.login(request, user)
        request.session.set_expiry(60 * 60 * 24 * 365 * 10 if remember else 0)
        return True


class Email(models.Model):
    date_created = models.DateTimeField(u"Créé le", auto_now_add=True)
    name = models.CharField(u"Nom", max_length=254)
    subject = models.CharField(u"Sujet du mail", max_length=254, blank=True, null=True)
    receivers = models.TextField(u"Adresses emails", blank=True, null=True)
    template = models.TextField(u"Template du mail")
    template_name = models.TextField(u"Template name", blank=True, null=True)
    is_sent = models.BooleanField(u"Envoyé ?", default=False)

    class Meta:
        verbose_name = u"Email groupé"
        verbose_name_plural = u"Emails groupés"
        ordering = ('-date_created',)

    def __unicode__(self):
        return u"{0} - {1}".format(self.name, self.email)

    def send_test(self, force=False):
        receivers = []
        activate_url = re.search(r'\*\|ACTIVATE_URL\|\*', self.template)

        for email in list(set(TestEmail.objects.all().values_list('email', flat=True))):
            html = self.template

            if activate_url:
                print activate_url, activate_url.group(0)

                activation_token, created = UserActivationToken.objects.get_or_create(email=email)
                html = html.replace(activate_url.group(0), activation_token.get_activate_url() )

            email_context = {
                'user': self,
            }
            send_html_email(
                self.subject,
                settings.DEFAULT_NO_REPLY_EMAIL,
                [email],
                html=html,
                context=email_context
            )
            receivers.append(email)
        return receivers

    def send(self, force=False):
        receivers = []

        # if not self.is_sent:
        #     template = self.template
        #     activate_url = re.search(r'\{\{\s*activate_url\s*\}\}', template)

        #     if activate_url:

        #         activation_token, created = UserActivationToken.get_or_create(email=email)

        #         template.replace()

        #     email_context = {
        #         'user': self,
        #     }
        #     email_context.update(context)
        #     send_html_email(
        #         subject,
        #         settings.DEFAULT_NO_REPLY_EMAIL,
        #         [self.email],
        #         template=template,
        #         context=email_context
        #     )
        #     self.is_sent = True
        #     self.save()
        #     return True
        return receivers

class EmailTransaction(models.Model):

    email = models.ForeignKey('emailing.Email')
    date_created = models.DateTimeField(u"Créé le", auto_now_add=True)
    receiver = models.EmailField(u"Adresse email", max_length=254)
    is_sent = models.BooleanField(u"Envoyé ?", default=False)

    class Meta:
        verbose_name = u"Transaction"
        verbose_name_plural = u"Transactions"
        ordering = ('-date_created',)

    def __unicode__(self):
        return u"{0} - {1}".format(self.name, self.email)

    def send(self, force=False):

        if not self.is_sent:
            template = self.template

            activate_url = re.search(r'\{\{\s*activate_url\s*\}\}', template)
            if activate_url:
                template.replace()

            email_context = {
                'user': self,
            }
            email_context.update(context)
            send_html_email(
                subject,
                settings.DEFAULT_NO_REPLY_EMAIL,
                [self.email],
                template=template,
                context=email_context
            )
            self.is_sent = True
            self.save()
            return True
        return False


class TestEmail(models.Model):
    email = models.EmailField(u"Adresse email", max_length=254)






