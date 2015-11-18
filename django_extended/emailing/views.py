# encoding: utf-8
from django.conf import settings
from django.views import generic
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from .models import *

class Activate(generic.View):

    def get(self, request, token, *args, **kwargs):
        try:
            token = EmailingUserActivationToken.objects.get(token=token)
            user = token.activate_user()
            if user:
                if token.authenticate_user(request, user, remember=True):
                    messages.success(request, u"Votre inscription est confirmée.<br /> Bienvenue sur Ubbik !")
                    return HttpResponseRedirect(reverse('user:dashboard'))

        except EmailingUserActivationToken.DoesNotExist:
            pass
        raise Http404