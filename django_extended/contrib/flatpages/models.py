# encoding: utf-8

from django.db import models
from django.utils.html import strip_tags
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from fields_bundle.fields import HTMLField
from taggit_autosuggest.managers import TaggableManager as AutosuggestTaggableManager


class FlatPagePosition(models.Model):

    flatpage = models.ForeignKey("flatpage.FlatPage", verbose_name="Page statique", related_name="positions")
    PLACEMENT_HEADER = 'HEADER'
    PLACEMENT_FOOTER = 'FOOTER'
    PLACEMENT_CHOICES = (
        (PLACEMENT_HEADER, u"Haut de page"),
        (PLACEMENT_FOOTER, u"Pied de page"),
    )
    placement = models.CharField("Position", max_length=254, choices=PLACEMENT_CHOICES, default=PLACEMENT_FOOTER)
    order = models.PositiveIntegerField(u"Ordre d'affichage", default=1)
    order_col = models.PositiveIntegerField(u"Ordre Colonne", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name=u"Activée ?")

    class Meta:
        verbose_name = u"Position d'un lien de page statique"
        verbose_name_plural = u"Positions des page statique"
        ordering = ('placement' ,'order_col', 'order',  )

class FlatPage(models.Model):

    created_date = models.DateTimeField(u"Date created", auto_now_add=True)
    updated_date = models.DateTimeField(u"Date updated", auto_now=True, db_index=True)

    title = models.CharField(u"Titre", max_length=254)
    link_name = models.CharField(u"Nom du lien", max_length=254, blank=True, null=True)

    LINK_TYPE_PAGE = "PAGE"
    LINK_TYPE_APP = "APP"
    LINK_TYPE_EXTERNAL = "EXTERNAL"
    LINK_TYPE_CHOICES = (
        (LINK_TYPE_PAGE, u"Page HTML"),
        (LINK_TYPE_APP, u"Page interne existante"),
        (LINK_TYPE_EXTERNAL, u"Page externe"),
    )
    link_type = models.CharField(u"Type de page", max_length=254, choices=LINK_TYPE_CHOICES, default=LINK_TYPE_PAGE)
    link_value = models.CharField(u"URL", max_length=254, blank=True, null=True)


    meta_title = models.CharField(u"Meta - Titre", max_length=254, blank=True, null=True)
    meta_description = models.CharField(u"Meta - Description", max_length=254, blank=True, null=True)
    tags = AutosuggestTaggableManager(verbose_name="Tags", help_text=u"Séparez par une virgule ou utilisez la touche tabulation.", blank=True)

    content = HTMLField(u"Contenu", blank=True)
    is_active = models.BooleanField(default=True, verbose_name=u"Activée ?")
    slug = models.CharField(u"Url de la page", max_length=254, default="", blank=True, help_text=u"auto générée, ne changer que si conflits d'url")



    class Meta:
        verbose_name = u"Page statique"
        verbose_name_plural = u"Pages statiques"
        ordering = ('title',  )

    @models.permalink
    def get_absolute_url(self):
        return ('flatpage:view', (), {'slug': self.slug })

    def get_url(self):

        if self.link_value:
            if self.link_type == FlatPage.LINK_TYPE_APP:
                if self.link_value.find(':') != -1:
                    return reverse(self.link_value)
                else:
                    return self.link_value
            elif self.link_type == FlatPage.LINK_TYPE_EXTERNAL:
                if not self.value.startsWith('http://') or \
                    not self.value.startsWith('https://'):
                    self.link_value = "http://" % self.link_value
                return self.link_value
        else:
            return self.get_absolute_url()
            # return reverse(*reverse_url)


    def get_tags(self):
        return [ tag.strip() for tag in re.split(r"[\|,:;#!\.\-_]+", self.tags)]

    def __unicode__(self):
        return self.title

    def save(self, **kwargs):
        if not self.slug or self.slug.strip().strip('/') == "":
            self.slug = slugify(self.title)
        self.slug = "/".join([ slugify(slug) for slug in self.slug.split('/') ])
        if self.slug.strip('/').startswith('admin'):
            self.slug = self.slug.replace('admin', '__admin')
        if not self.link_name and self.title:
            self.link_name = self.title
        super(FlatPage, self).save(**kwargs)





class Settings(models.Model):



    class Meta:
        verbose_name = u"Paramètre"
        verbose_name_plural = u"Paramètres"

    def __unicode__(self):
        return u"Paramètres"

    def save(self, *args, **kwargs):
        if Settings.objects.count():
            Settings.objects.first().delete()
        super(Settings, self).save(*args, **kwargs)

    @staticmethod
    def get_settings():
        settings = Settings.objects.first()
        if not settings:
            settings = Settings()
            settings.save()
        return settings