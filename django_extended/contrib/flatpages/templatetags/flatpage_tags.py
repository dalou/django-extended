# encoding: utf-8

import datetime

from django import template
from django.conf import settings
from django.db.models import Count
from django.utils import timezone
from taggit_templatetags.templatetags.taggit_extras import get_queryset

register = template.Library()

from ..models import *

@register.inclusion_tag('flatpage/_list_footer.html')
def flatpage_list_footer(flat=False):
    positions = FlatPagePosition.objects.select_related('flatpage').filter(
        is_active=True,
        flatpage__is_active=True,
        placement=FlatPagePosition.PLACEMENT_FOOTER
    )
    return {
        'cols': [1,2,3,4,5,6],
        'flat': flat,
        'positions': positions
    }

@register.inclusion_tag('flatpage/_list_header.html')
def flatpage_list_header(flat=False):
    positions = FlatPagePosition.objects.select_related('flatpage').filter(
        is_active=True,
        flatpage__is_active=True,
        placement=FlatPagePosition.PLACEMENT_HEADER
    )
    return {
        'flat': flat,
        'positions': positions,
    }