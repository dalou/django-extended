# encoding: utf-8
import re

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils import timezone
from taggit.managers import TaggableManager
from fields_bundle.fields import JSONField, PriceField, HTMLField, CroppedImageField
from libs.utils import unique_filename, geocode

# class Category(models.Model):
#     date_created = models.DateTimeField(_(u"Date création"), auto_now_add=True)
#     date_updated = models.DateTimeField(_(u"Date mise à jour"), auto_now=True,
#         db_index=True)
#     name = models.CharField(_(u"Nom"), max_length=254)
#     slug = models.SlugField(_(u"Slug"), max_length=254, default="", blank=True)
#     meta_title = models.CharField(_(u"Meta title"), max_length=254,
#         blank=True, null=True)
#     description = models.CharField(_(u"Description + Meta desc"),
#         max_length=254, blank=True, null=True)
#     theme_color = ColorField(_(u"Theme couleur"),
#         max_length=254, help_text=_(u"rgb(r,g,b,a) ou #RRGGBB"),
#         blank=True, null=True)
#     theme_icon = models.CharField(_(u"Theme icône"), max_length=254,
#         blank=True, null=True)
#     tags = TaggableManager(blank=True, verbose_name="Tags",
#                            help_text="Séparés par une virgule.",)
#     editable = models.BooleanField(_(u"Editable?"), default=True)
#     order = models.PositiveIntegerField(_(u"Ordre d'affichage"),
#         default=0, help_text=_(u"Position d'affichage"))

#     class Meta:
#         verbose_name = _(u"Catégorie de Blog")
#         ordering = ('order', 'name')

#     def save(self, **kwargs):
#         self.slug = slugify(self.name)
#         super(Category, self).save(**kwargs)

#     def __unicode__(self):
#         return self.name


class Post(models.Model):

    is_post = True

    created_date = models.DateTimeField(u"Date created", auto_now_add=True)
    updated_date = models.DateTimeField(u"Date updated", auto_now=True, db_index=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owned_posts", null=True, blank=True)
    organization = models.ForeignKey('organization.Organization', related_name="posts", null=True, blank=True)
    group = models.ForeignKey('group.Group', related_name="posts", null=True, blank=True)

    title = models.CharField(u'Titre', max_length=254)
    slug = models.SlugField(u"Slug", max_length=255)

    meta_title = models.CharField(u"Meta titre", max_length=254, blank=True, null=True)
    meta_description = models.TextField(u"Meta description", max_length=254, blank=True, null=True)
    content = HTMLField(u"Contenu de l'article")

    STATUS_NEW, STATUS_REJECTED, STATUS_VALIDATED, STATUS_EXPIRED, STATUS_DISABLED = ('NEW', 'REJECTED', 'VALIDATED', 'EXPIRED', 'DISABLED')
    STATUS_CHOICES = (
        (STATUS_NEW, u"En attente de validation"),
        (STATUS_REJECTED, u"Rejetée"),
        (STATUS_VALIDATED, u"Validée"),
        (STATUS_EXPIRED, u"Expirée"),
        (STATUS_DISABLED, u"Désactivée")
    )
    status = models.CharField(max_length=254, choices=STATUS_CHOICES, default=STATUS_NEW, verbose_name=u"Status", null=False, blank=False)

    published_date = models.DateTimeField(verbose_name=u"Date de publication", default=timezone.now)
    is_published = models.BooleanField(u"Publié ?", default=True)
    is_fake = models.BooleanField(u"Fake ?", default=False)


    tags = TaggableManager(verbose_name="Tags", help_text="Séparés par une virgule.", blank=True)
    # order = models.PositiveIntegerField(u"Ordre d'affichage", default=0)

    # category = models.ForeignKey('blog.Category', related_name="blogposts",
    #     verbose_name=_(u"Catégorie"))

    class Meta:
        verbose_name = u"Actualité"
        ordering = ('-published_date',)

    @models.permalink
    def get_absolute_url(self):
        return ('blog:post-view', (), {'slug': self.slug, 'pk': self.pk })

    def __unicode__(self):
        return self.title

    def save(self, **kwargs):
        self.slug = slugify(u"%s" % (self.title))
        super(Post, self).save(**kwargs)
