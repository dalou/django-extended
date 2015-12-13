# encoding: utf-8

from django.conf import settings
from django.db import models
from django.utils.text import slugify

from django import forms
from itertools import chain

class Tree(models.Model):

    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    order = models.IntegerField(u"Ordre", default=0)
    level = models.PositiveIntegerField(u"Profondeur", default=0)

    is_required = models.BooleanField(u"Requit ?", default=False)
    is_independant = models.BooleanField(u"Indépendant ?", default=False)
    is_multiple = models.BooleanField(u"Choix multiple ?", default=False)

    class Meta:
        abstract = True
        ordering = ('-level', 'order', )
        verbose_name = u'Catégorie'
        verbose_name_plural = u'Catégories'


    def save(self, *args, **kwargs):
        if self.parent:
            self.level = self.parent.level + 1
        super(Tree, self).save(*args, **kwargs)

    def get_descendants(self, include_self=False):
        return self.children.all()
