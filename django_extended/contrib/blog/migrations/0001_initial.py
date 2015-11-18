# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import taggit.managers
import fields_bundle.fields.html


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('group', '0004_auto_20151110_0615'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0028_auto_20151110_0615'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Date updated', db_index=True)),
                ('title', models.CharField(max_length=254, verbose_name='Titre')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('meta_title', models.CharField(max_length=254, null=True, verbose_name='Meta titre', blank=True)),
                ('meta_description', models.TextField(max_length=254, null=True, verbose_name='Meta description', blank=True)),
                ('content', fields_bundle.fields.html.HTMLField(verbose_name="Contenu de l'article")),
                ('status', models.CharField(default=b'NEW', max_length=254, verbose_name='Status', choices=[(b'NEW', 'En attente de validation'), (b'REJECTED', 'Rejet\xe9e'), (b'VALIDATED', 'Valid\xe9e'), (b'EXPIRED', 'Expir\xe9e'), (b'DISABLED', 'D\xe9sactiv\xe9e')])),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de publication')),
                ('is_published', models.BooleanField(default=True, verbose_name='Publi\xe9 ?')),
                ('is_fake', models.BooleanField(default=False, verbose_name='Fake ?')),
                ('group', models.ForeignKey(related_name='posts', blank=True, to='group.Group', null=True)),
                ('organization', models.ForeignKey(related_name='posts', blank=True, to='organization.Organization', null=True)),
                ('owner', models.ForeignKey(related_name='owned_posts', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text=b'S\xc3\xa9par\xc3\xa9s par une virgule.', verbose_name=b'Tags')),
            ],
            options={
                'ordering': ('-published_date',),
                'verbose_name': 'Actualit\xe9',
            },
        ),
    ]
