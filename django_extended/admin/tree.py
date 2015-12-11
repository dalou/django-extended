# encoding: utf-8

import datetime
import operator
import re

from django import forms
from django.conf import settings
from django.contrib import admin



class TreeAdmin(admin.ModelAdmin):


    list_per_page = 500
    list_display = (
        'parent',
        'order',
        'is_required',
        'is_independant',
    )
    list_editable = ('is_required', 'is_independant', 'order', 'parent')



    class Media:
        css = {
            'all': ['vendors/select2/4.0.0/css/select2.min.css']
        }
        js = (
            'vendors/select2/4.0.0/js/select2.min.js',
            # 'vendors/jquery-ui-1.8.16.custom.min.js',
            'vendors/jquery.mjs.nestedSortable.js',
            'libs/admin/categories.js',
            #'catalogue/js/admin/category/save.js',
        )

    def get_changelist_form(self, request, **kwargs):
        kwargs.setdefault('form', self.form)
        return super(CategoryAdmin, self).get_changelist_form(request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        return super(CategoryAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        return (super(TreeAdmin, self).get_queryset(request)
            .prefetch_related('children')
            .select_related('parent')
        )