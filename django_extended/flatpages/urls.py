# encoding: utf-8
from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^(?P<slug>[-\\\/_\w\d]+)/$', views.View.as_view(), name='view'),
]