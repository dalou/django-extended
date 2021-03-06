from __future__ import unicode_literals
from email.utils import parseaddr
import functools
try:
    from urllib.parse import urlparse, urlunparse
except ImportError:  # python 2
    from urlparse import urlparse, urlunparse
from django.conf import settings
from django.core import urlresolvers
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseRedirect, QueryDict
from django.contrib.auth import get_user_model

def is_valid_email(email):
    result = parseaddr(email.strip())
    if '@' in result[1]:
        return result[1]
    else:
        return None

def get_or_create_user(email, username=None, first_name=None, last_name=None,
                        is_active=False, expiration_date=None, set_names_from_email=False,
                        password=None, save=True):
    User = get_user_model()
    if email:
        email = is_valid_email(email)
        if email:
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                user = User(
                    email = email.strip(),
                    username = username.strip() if username else None,
                    first_name = first_name.strip() if first_name else None,
                    last_name = last_name.strip() if last_name else None,
                    is_active = is_active,
                    expiration_date = expiration_date
                )
                if password:
                    user.set_password(password)
                else:
                    user.set_unusable_password()
                if set_names_from_email:

                    if not user.username:
                        user.username = email.split('@')[0][0:254]

                    if not user.first_name and not user.last_name:
                        user_names = user.username.split('.', 2)
                        if len(user_names) == 2:
                            user.first_name = ''.join([i for i in user_names[0].capitalize() if not i.isdigit()])
                            user.last_name = ''.join([i for i in user_names[1].capitalize() if not i.isdigit()])
                        else:
                            user.first_name = ''.join([i for i in user_names[0].capitalize() if not i.isdigit()])
                if save:
                    user.save()
            return user
        else:
            return None
    else:
        return None

def get_user_lookup_kwargs(kwargs):
    result = {}
    username_field = getattr(get_user_model(), "USERNAME_FIELD", "username")
    for key, value in kwargs.items():
        result[key.format(username=username_field)] = value
    return result


def default_redirect(request, fallback_url, **kwargs):
    redirect_field_name = kwargs.get("redirect_field_name", "next")
    next_url = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name))
    if not next_url:
        # try the session if available
        if hasattr(request, "session"):
            session_key_value = kwargs.get("session_key_value", "redirect_to")
            if session_key_value in request.session:
                next_url = request.session[session_key_value]
                del request.session[session_key_value]
    is_safe = functools.partial(
        ensure_safe_url,
        allowed_protocols=kwargs.get("allowed_protocols"),
        allowed_host=request.get_host()
    )
    if next_url and is_safe(next_url):
        return next_url
    else:
        try:
            fallback_url = urlresolvers.reverse(fallback_url)
        except urlresolvers.NoReverseMatch:
            if callable(fallback_url):
                raise
            if "/" not in fallback_url and "." not in fallback_url:
                raise
        # assert the fallback URL is safe to return to caller. if it is
        # determined unsafe then raise an exception as the fallback value comes
        # from the a source the developer choose.
        is_safe(fallback_url, raise_on_fail=True)
        return fallback_url

def user_display(user):
    return settings.ACCOUNT_USER_DISPLAY(user)


def ensure_safe_url(url, allowed_protocols=None, allowed_host=None, raise_on_fail=False):
    if allowed_protocols is None:
        allowed_protocols = ["http", "https"]
    parsed = urlparse(url)
    # perform security checks to ensure no malicious intent
    # (i.e., an XSS attack with a data URL)
    safe = True
    if parsed.scheme and parsed.scheme not in allowed_protocols:
        if raise_on_fail:
            raise SuspiciousOperation("Unsafe redirect to URL with protocol '{0}'".format(parsed.scheme))
        safe = False
    if allowed_host and parsed.netloc and parsed.netloc != allowed_host:
        if raise_on_fail:
            raise SuspiciousOperation("Unsafe redirect to URL not matching host '{0}'".format(allowed_host))
        safe = False
    return safe


def handle_redirect_to_login(request, **kwargs):
    login_url = kwargs.get("login_url")
    redirect_field_name = kwargs.get("redirect_field_name")
    next_url = kwargs.get("next_url")
    if login_url is None:
        login_url = settings.ACCOUNT_LOGIN_URL
    if next_url is None:
        next_url = request.get_full_path()
    try:
        login_url = urlresolvers.reverse(login_url)
    except urlresolvers.NoReverseMatch:
        if callable(login_url):
            raise
        if "/" not in login_url and "." not in login_url:
            raise
    url_bits = list(urlparse(login_url))
    if redirect_field_name:
        querystring = QueryDict(url_bits[4], mutable=True)
        querystring[redirect_field_name] = next_url
        url_bits[4] = querystring.urlencode(safe="/")
    return HttpResponseRedirect(urlunparse(url_bits))


def get_form_data(form, field_name, default=None):
    if form.prefix:
        key = "-".join([form.prefix, field_name])
    else:
        key = field_name
    return form.data.get(key, default)
