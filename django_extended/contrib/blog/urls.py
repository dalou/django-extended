from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = patterns('',

    # url(r'^blog/articles/$', views.List.as_view(), name="list"),
    # url(r'^evenement/(?P<pk>[\d]+)/commenter/$', views.Participate.as_view(), name="participate"),
    url(r'^blog/article/(?P<pk>[\d]+)/(?P<slug>[-_\w]+)/$', views.View.as_view(), name="post-view"),


)