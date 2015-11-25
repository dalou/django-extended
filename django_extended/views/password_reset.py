# encoding: utf-8

from django import forms
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.sites.models import get_current_site
from django.contrib.auth.tokens import default_token_generator
from ..models import *


class PasswordResetForm(forms.Form):

    email = forms.EmailField(label=_("Email"), required=True)

    def clean_email(self):
        User = get_user_model()
        value = self.cleaned_data["email"]
        if not User.objects.filter(email__iexact=value).exists():
            raise forms.ValidationError(_("Email address can not be found."))
        return value


class PasswordReset(generic.FormView):

    template_name = "account/password_reset.html"
    template_name_sent = "account/password_reset_sent.html"
    form_class = PasswordResetForm
    token_generator = default_token_generator

    def get_context_data(self, **kwargs):
        context = kwargs
        if self.request.method == "POST" and "resend" in self.request.POST:
            context["resend"] = True
        return context

    def form_valid(self, form):
        self.send_email(form.cleaned_data["email"])
        response_kwargs = {
            "request": self.request,
            "template": self.template_name_sent,
            "context": self.get_context_data(form=form)
        }
        return self.response_class(**response_kwargs)

    def send_email(self, email):
        User = get_user_model()
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        current_site = get_current_site(self.request)
        email_qs = EmailAddress.objects.filter(email__iexact=email)
        for user in User.objects.filter(pk__in=email_qs.values("user")):
            uid = int_to_base36(user.id)
            token = self.make_token(user)
            password_reset_url = "{0}://{1}{2}".format(
                protocol,
                current_site.domain,
                reverse("account_password_reset_token", kwargs=dict(uidb36=uid, token=token))
            )
            ctx = {
                "user": user,
                "current_site": current_site,
                "password_reset_url": password_reset_url,
            }
            hookset.send_password_reset_email([user.email], ctx)

    def make_token(self, user):
        return self.token_generator.make_token(user)

