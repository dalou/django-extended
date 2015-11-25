# encoding: utf-8
from django import forms
from django.conf import settings
from django.views import generic
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone
from .. import signals
from ..utils.user import default_redirect, get_or_create_user

# from django_flow.utils import send_staff_notification, send_template_email

User = get_user_model()

class SignupForm(forms.Form):

    first_name = forms.CharField(
        label=u"Prénom",
        required=False
    )

    last_name = forms.CharField(
        label=u"Nom",
        required=False
    )

    email = forms.EmailField(
        label=u"* Adresse e-mail",
        widget=forms.TextInput(),
        required=True,
    )

    username = forms.CharField(
        label=u"* Nom d'utilisateur / Pseudo",
        required=True
    )

    password = forms.CharField(
        label=u"* Mot de passe",
        widget=forms.PasswordInput(render_value=True)
    )

    password_confirm = forms.CharField(
        label=u"* Confirmer le mot de passe",
        widget=forms.PasswordInput(render_value=False)
    )

    accept_terms = forms.BooleanField(
        label=u"""J'accepte les <a data-modal="/conditions-dutilisation/" href="/conditions-dutilisation/">conditions d'utilisation d'Ubbik</a>""" ,
        required=False
    )

    def clean_email(self):
        value = self.cleaned_data["email"]
        if not User.objects.filter(email__iexact=value).exists():
            return value
        raise forms.ValidationError(u"Un utilisateur est déjà enregistré avec cet adresse e-mail.")

    def clean_accept_terms(self):
        value = self.cleaned_data.get("accept_terms")
        # if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
        if not value:
            raise forms.ValidationError(u"Vous devez accepter les conditions d'utilisations.")
        return value

    def clean_password_confirm(self):
        value = self.cleaned_data["password_confirm"].strip()
        # if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
        if self.cleaned_data["password"].strip() != value:
            raise forms.ValidationError(u"Le mot de passe doit être le même.")
        return value

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        # del self.fields["username"]
        self.fields.keyOrder = ['email', 'password', 'password_confirm']


class Signup(generic.FormView):

    template_name = "user/signup.html"
    #template_name_ajax = "user/_signup.html"
    form_class = SignupForm

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(reverse('user:dashboard'))
        # if not self.is_open():
        #     return self.closed()
        return super(Signup, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            raise Http404()
        # if not self.is_open():
        #     return self.closed()
        return super(Signup, self).post(*args, **kwargs)

    def get_initial(self):
        initial = super(Signup, self).get_initial()
        # if self.is_invitation:
        #     initial["invitation_hash"] = self.get_invitation_hash()
        if self.request.GET.get('email'):
            initial["email"] = self.request.GET.get('email')
        return initial

    def form_valid(self, form):

        user = get_or_create_user(
            form.cleaned_data["email"],
            username = form.cleaned_data["username"],
            first_name = form.cleaned_data["first_name"],
            last_name = form.cleaned_data["last_name"],
            is_active = False,
            expiration_date = timezone.now(),
            password = form.cleaned_data.get("password"),
            save = True
        )
        user.send_activation_email()
        return redirect(self.get_success_url())


    def form_invalid(self, form):
        signals.user_sign_up_attempt.send(
            sender=SignupForm,
            email=form.cleaned_data.get("email"),
            result=form.is_valid()
        )
        return super(Signup, self).form_invalid(form)

    def get_success_url(self, fallback_url=None, **kwargs):

        return reverse('main:home')
