# encoding: utf-8
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = patterns('',
    url(r"^user/activation/(?P<token>\w{10,64})/$", views.Activate.as_view(), name="activate-user"),
)