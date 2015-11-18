# encoding: utf-8

from django.conf import settings
from django import forms
from django.db.models import Q, Count
from django.views import generic
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from ..models import *
from apps.main.paginator import DiggPaginator

class View(generic.DetailView):
    template_name = "post/view.html"
    context_object_name = 'event'
    model = Post
    event = None

    def get(self, request, *args, **kwargs):
        # if not self.request.is_ajax():
        #     return HttpResponseRedirect("%s#product=%s" % (reverse('product:list'), self.kwargs.get('pk')))
        return super(View, self).get(request, *args, **kwargs)
