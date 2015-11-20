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
from django.contrib.auth import get_user_model
from django.utils import timezone

from .utils import *



class EmailingUserActivationToken(models.Model):

    created_date = models.DateTimeField(u"Créé le", auto_now_add=True)
    updated_date = models.DateTimeField(u"Modifié le", auto_now=True, db_index=True)

    email = models.EmailField(u"Adresse email", max_length=254, unique=True, db_index=True)
    token = models.CharField(u"Token d'activation", max_length=64, unique=True, db_index=True)
    is_used = models.BooleanField(u'Utilisé ?', default=False)
    expiration_date = models.DateTimeField(u"date d'expiration", blank=True, null=True)
    activation_date = models.DateTimeField(u"date d'activation", blank=True, null=True)

    _hash_func = hashlib.sha256


    class Meta:
        verbose_name = u"Clé d'activation"
        verbose_name_plural = u"Clés d'activation"
        ordering = ('-activation_date',)

    def save(self, **kwargs):
        if not self.token:
            bits = [self.email, str(random.SystemRandom().getrandbits(512))]
            self.token =  self._hash_func("".join(bits).encode("utf-8")).hexdigest()
        super(EmailingUserActivationToken, self).save(**kwargs)

    def activate_user(self):
        User = get_user_model()
        self.email = self.email.strip()
        if is_valid_email(self.email):
            try:

                user = User.objects.get(email__iexact=self.email)
                if not user.is_active:
                    user.is_active = True
                    user.save()

                if self.is_used:
                    return user

            except User.DoesNotExist:

                user = User(
                    email=self.email,
                    is_active=True,
                    username=self.email.split('@')[0][0:254]
                )
                user.set_unusable_password()
                user.save()

            self.is_used = True
            self.activation_date = timezone.now()
            self.save()
            return user

        return None

    def get_activate_url(self):
        return "{0}://{1}{2}".format(
            getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http"),
            Site.objects.get_current(),
            reverse("django_extended-emailing_activate_user", args=[self.token])
        )

    def authenticate_user(self, request, user, remember=False):
        if not hasattr(user, 'backend'):
            user.backend = 'apps.user.auth.AuthModelBackend'
        if request.user.is_authenticated():
            auth.logout(request)
        auth.login(request, user)
        request.session.set_expiry(60 * 60 * 24 * 365 * 10 if remember else 0)
        return True


class Emailing(models.Model):
    created_date = models.DateTimeField(u"Créé le", auto_now_add=True)
    updated_date = models.DateTimeField(u"Modifié le", auto_now=True, db_index=True)

    name = models.CharField(u"Nom", max_length=254)
    subject = models.CharField(u"Sujet du mail", max_length=254, blank=True, null=True)
    sender = models.CharField(u"De", max_length=254, blank=True, null=True)
    receivers = models.TextField(u"Vers (destinations réélles)", blank=True, null=True)
    receivers_test = models.TextField(u"Vers (destination de test)", blank=True, null=True)
    template = models.TextField(u"Template")
    # template_name = models.TextField(u"Template name", blank=True, null=True)
    send_count = models.IntegerField(u"Compteur d'envois", default=0)
    test_count = models.IntegerField(u"Compteur de tests", default=0)

    class Meta:
        verbose_name = u"Email groupé"
        verbose_name_plural = u"Emails groupés"
        ordering = ('-created_date',)

    def __repr__(self):
        sent = ""
        if self.send_count > 0:
            sent = u" (Envoyé)"
        return u"{0} - {1}{2}".format(self.name, self.subject, sent)


    def send(self, force=False, test=True):
        final_receivers = []
        if self.pk:
            activate_url = re.search(r'\*\|ACTIVATE_URL\|\*', self.template)
            archive_url = re.search(r'\*\|ARCHIVE\|\*', self.template)
            mc_subject = re.search(r'\*\|MC:SUBJECT\|\*', self.template)

            receivers = self.receivers_test if test else self.receivers
            receivers = receivers.split(',')
            messages = []

            for receiver in receivers:
                receiver = receiver.strip()
                if is_valid_email(receiver):

                    html = self.template
                    html = set_mailchimp_vars(html)

                    if activate_url:
                        activation_token, created = EmailingUserActivationToken.objects.get_or_create(email=receiver)
                        html = html.replace(activate_url.group(0), activation_token.get_activate_url() )

                    # if archive_url:
                    #     html = html.replace(archive_url.group(0), self. )

                    if mc_subject:
                        html = html.replace(mc_subject.group(0), self.subject )

                    html = clean_html_for_email(html)

                    if not test:
                        transaction, created = EmailingTransaction.objects.get_or_create(
                            receiver=receiver,
                            emailing=self
                        )
                    else:
                        created = True
                    if created or transaction.send_count == 0:
                        message = HtmlTemplateEmail(
                            subject=self.subject,
                            sender=self.sender,
                            receivers=[receiver],
                            html=html,
                        )
                        messages.append(message)
                        final_receivers.append(receiver)
                        if not test:
                            transaction.send_count += 1
                            transaction.save()

            send_mass_email(messages)
            if test:
                self.test_count += 1
            else:
                self.send_count += 1
            self.save()
        return final_receivers



class EmailingTransaction(models.Model):

    created_date = models.DateTimeField(u"Créé le", auto_now_add=True)
    updated_date = models.DateTimeField(u"Modifié le", auto_now=True, db_index=True)

    emailing = models.ForeignKey('django_extended.Emailing')
    receiver = models.EmailField(u"Adresse email", max_length=254)
    send_count = models.IntegerField(u"Compteur d'envois", default=0)

    class Meta:
        verbose_name = u"Email - Transaction"
        verbose_name_plural = u"Email - Transactions"
        ordering = ('-created_date',)

    def __unicode__(self):
        sent = ""
        if self.send_count > 0:
            sent = u" (Envoyé)"
        return u"{0}{1}".format(self.emailing.name, sent)



class EmailingTestEmail(models.Model):
    email = models.EmailField(u"Adresse email", max_length=254)






