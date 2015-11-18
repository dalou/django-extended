from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address, DEFAULT_ATTACHMENT_MIME_TYPE
from django.core.mail.backends.smtp import EmailBackend

from .models import *

class DevBackend(EmailBackend):

    def route_recipients(self, recipients):
        for i,r in enumerate(recipients):
            recipients[i] = "autrusseau.damien@gmail.com"
        return recipients

    def _send(self, message):
        message.to = self.route_recipients(message.to)
        message.cc = self.route_recipients(message.cc)
        message.bcc = self.route_recipients(message.bcc)
        super(DevBackend, self)._send(message)


class ProductionBackend(EmailBackend):

    def route_recipients(self, recipients):
        if getattr(settings, 'EMAIL_DOMAIN_ONLY', False):
            receivers = ", ".join(list(set(TestEmail.objects.all().values_list('email', flat=True))))
            # for i,r in enumerate(recipients):
            #     if not r.endswith('@%s' % PROJECT_DOMAIN):
            #         recipients = settings.DEFAULT_FROM_EMAIL
        return recipients

    def _send(self, message):
        if getattr(settings, 'EMAIL_DOMAIN_ONLY', False):
            message.to = self.route_recipients(message.to)
            message.cc = self.route_recipients(message.cc)
            message.bcc = self.route_recipients(message.bcc)
        super(ProductionBackend, self)._send(message)