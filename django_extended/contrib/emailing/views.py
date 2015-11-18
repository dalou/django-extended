# encoding: utf-8
from django.conf import settings
from django.views import generic
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
User = get_user_model()

class Activate(generic.View):

    def get(self, request, token, *args, **kwargs):
        try:
            token = UserActivationToken.objects.get(token=token)

            User = get_user_model()
            if token.email:
                token.email = is_valid_email(token.email)
                if token.email:
                    try:
                        user = User.objects.get(email__iexact=token.email)
                    except User.DoesNotExist:
                        user = User(
                            email=token.email.strip(),
                            is_active=True,
                        )
                        if password:
                            user.set_password(password)
                        else:
                            user.set_unusable_password()

                        if not user.username:
                            user.username = email.split('@')[0][0:254]
                        user.save()
                else:
                    return None
            else:
                return None


            if user.activate():
                if user.authenticate(request, remember=True):
                    messages.success(request, u"Votre inscription est confirmée.<br /> Bienvenue sur Ubbik !")
                    return HttpResponseRedirect(reverse('user:dashboard'))

        except UserActivationToken.DoesNotExist:
            pass
        raise Http404