# encoding: utf-8
from django.views import generic
from django.http import Http404, HttpResponseRedirect

from .models import *


class View(generic.detail.DetailView):
    template_name = 'flatpage/view.html'
    template_name_ajax = 'flatpage/_view.html'
    context_object_name = 'flatpage'
    model = FlatPage
    slug_field = 'slug'

    def get_template_names(self):
        if self.request.is_ajax():
            return self.template_name_ajax
        else:
            return self.template_name

    def get(self, *args, **kwargs):

        object = self.get_object()
        if object.link_type in [
            FlatPage.LINK_TYPE_APP,
            FlatPage.LINK_TYPE_EXTERNAL
        ]:
            return HttpResponseRedirect(object.get_url())

        return super(View, self).get(*args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(View, self).get_object(queryset)
        if obj is None:
            raise Http404('Page inexistante')
        return obj

    def get_context_data(self, **kwargs):
        ctx = super(View, self).get_context_data(**kwargs)
        return ctx
