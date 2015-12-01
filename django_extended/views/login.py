# encoding: utf-8

from django import forms
from django.views import generic
from django.contrib import auth
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from ..utils.user import default_redirect
from .. import signals


class LoginForm(forms.Form):

    email = forms.EmailField(label="Adresse e-mail")
    authentication_fail_message = _(u"L'adresse email ou le mot de passe que vous avez renseigné est incorrect.")

    password = forms.CharField(
        label=u"Mot de passe",
        widget=forms.PasswordInput(render_value=True)
    )
    remember = forms.BooleanField(
        label=u"Se souvenir de moi",
        required=False
    )
    user = None

    def clean(self):
        if self._errors:
            return
        user = auth.authenticate(
            username=self.cleaned_data["email"],
            password=self.cleaned_data["password"]
        )
        if user:
            if user.is_active:
                self.user = user
            else:
                self.add_error('email', "This account is inactive.")
        else:
            self.add_error('email', self.authentication_fail_message)
        return self.cleaned_data


class Login(generic.FormView):
    template_name = "user/login.html"
    form_class = LoginForm
    form_kwargs = {}
    redirect_field_name = "next"

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(self.get_success_url())
        return super(Login, self).get(*args, **kwargs)

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.template_name_ajax]
        else:
            return [self.template_name]

    def get_context_data(self, **kwargs):
        ctx = kwargs
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.POST.get(redirect_field_name, self.request.GET.get(redirect_field_name, "")),
        })
        return ctx

    def get_form_kwargs(self):
        kwargs = super(Login, self).get_form_kwargs()
        kwargs.update(self.form_kwargs)
        return kwargs

    def form_invalid(self, form):

        if form.prefix:
            key = "-".join([form.prefix, "email"])
        else:
            key = "email"
        username = form.data.get(key, None)

        signals.user_login_attempt.send(
            sender=Login,
            username=username,
            result=form.is_valid()
        )
        return super(Login, self).form_invalid(form)

    def form_valid(self, form):
        form.user.authenticate(self.request, remember=form.cleaned_data.get("remember"))
        signals.user_logged_in.send(sender=Login, user=form.user, form=form)
        return redirect(self.get_success_url())


    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = '/'
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)

    def get_redirect_field_name(self):
        return self.redirect_field_name