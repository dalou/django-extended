# encoding: utf-8

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.filters import RelatedFieldListFilter
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe

from .models import *

class FlatPagePositionInline(admin.TabularInline):
    suit_classes = 'suit-tab suit-tab-positions'
    model = FlatPagePosition
    extra = 0

class FlatPageAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'url', 'is_active', 'positions', 'link_type',)
    inlines = (FlatPagePositionInline, )
    list_prefetch_related = ('positions', )
    ordering = ['-positions__placement', 'positions__order_col', 'positions__order']

    class Media:
        js = (
            'flatpage/admin.js',
        )


    suit_form_tabs = (
        ('settings', u"Paramètres"),
        ('positions', u"Positions des liens"),
        ('seo', u"SEO (réf)"),
    )

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-settings',),
            'fields': ( 'is_active', 'title', 'link_name', 'link_type', 'link_value', 'tags', 'content', )
        }),
        (u"SEO (réf)", {
            'classes': ('suit-tab suit-tab-seo',),
            'fields': ('meta_title', 'meta_description')
        }),
    )


    def url(self, obj):
        url = obj.get_url()
        return mark_safe('<a target="_blank" href="%s">%s</a>' % (url , url))
    url.short_description = "URL Finale"

    def positions(self, obj):
        return "<br />".join([ "<b>%s</b>, row:<b>%s</b>, col:<b>%s</>" % (position.get_placement_display(), position.order, position.order_col ) for position in obj.positions.all()])
    positions.short_description = "Positions des liens"
    positions.allow_tags = True

    def get_queryset(self, request):
        qs = super(FlatPageAdmin, self).get_queryset(request)
        return qs.distinct()
        # tqs = FlatPagePosition.objects.order_by('placement', 'order_col', 'order').values_list('pk', flat=True)
        # print tqs
        # qs = qs.filter(positions=tqs)
        # return qs

    def save_model(self, request, obj, form, change):
        obj.save()

admin.site.register(FlatPage, FlatPageAdmin)
