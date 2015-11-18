# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extended.fields.html
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emailing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Cr\xe9\xe9 le')),
                ('name', models.CharField(max_length=254, verbose_name='Nom')),
                ('subject', models.CharField(max_length=254, null=True, verbose_name='Sujet du mail', blank=True)),
                ('receivers', models.TextField(null=True, verbose_name='Adresses emails', blank=True)),
                ('template', models.TextField(verbose_name='Template du mail')),
                ('template_name', models.TextField(null=True, verbose_name='Template name', blank=True)),
                ('is_sent', models.BooleanField(default=False, verbose_name='Envoy\xe9 ?')),
            ],
            options={
                'ordering': ('-date_created',),
                'verbose_name': 'Email group\xe9',
                'verbose_name_plural': 'Emails group\xe9s',
            },
        ),
        migrations.CreateModel(
            name='EmailingTestEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Adresse email')),
            ],
        ),
        migrations.CreateModel(
            name='EmailingTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Cr\xe9\xe9 le')),
                ('receiver', models.EmailField(max_length=254, verbose_name='Adresse email')),
                ('is_sent', models.BooleanField(default=False, verbose_name='Envoy\xe9 ?')),
                ('email', models.ForeignKey(to='django_extended.Emailing')),
            ],
            options={
                'ordering': ('-date_created',),
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.CreateModel(
            name='EmailingUserActivationToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='Adresse email', db_index=True)),
                ('token', models.CharField(unique=True, max_length=64, verbose_name="Token d'activation", db_index=True)),
                ('is_used', models.BooleanField(default=False, verbose_name='Utilis\xe9 ?')),
                ('expiration_date', models.DateTimeField(null=True, verbose_name="date d'expiration", blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlatPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Date updated', db_index=True)),
                ('title', models.CharField(max_length=254, verbose_name='Titre')),
                ('link_name', models.CharField(max_length=254, null=True, verbose_name='Nom du lien', blank=True)),
                ('link_type', models.CharField(default=b'PAGE', max_length=254, verbose_name='Type de page', choices=[(b'PAGE', 'Page HTML'), (b'APP', 'Page interne existante'), (b'EXTERNAL', 'Page externe')])),
                ('link_value', models.CharField(max_length=254, null=True, verbose_name='URL', blank=True)),
                ('meta_title', models.CharField(max_length=254, null=True, verbose_name='Meta - Titre', blank=True)),
                ('meta_description', models.CharField(max_length=254, null=True, verbose_name='Meta - Description', blank=True)),
                ('content', django_extended.fields.html.HTMLField(verbose_name='Contenu', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Activ\xe9e ?')),
                ('slug', models.CharField(default=b'', help_text="auto g\xe9n\xe9r\xe9e, ne changer que si conflits d'url", max_length=254, verbose_name='Url de la page', blank=True)),
                ('tags', taggit_autosuggest.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='S\xe9parez par une virgule ou utilisez la touche tabulation.', verbose_name=b'Tags')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Page statique',
                'verbose_name_plural': 'Pages statiques',
            },
        ),
        migrations.CreateModel(
            name='FlatPagePosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('placement', models.CharField(default=b'FOOTER', max_length=254, verbose_name=b'Position', choices=[(b'HEADER', 'Haut de page'), (b'FOOTER', 'Pied de page')])),
                ('order', models.PositiveIntegerField(default=1, verbose_name="Ordre d'affichage")),
                ('order_col', models.PositiveIntegerField(null=True, verbose_name='Ordre Colonne', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Activ\xe9e ?')),
                ('flatpage', models.ForeignKey(related_name='positions', verbose_name=b'Page statique', to='django_extended.FlatPage')),
            ],
            options={
                'ordering': ('placement', 'order_col', 'order'),
                'verbose_name': "Position d'un lien de page statique",
                'verbose_name_plural': 'Positions des page statique',
            },
        ),
        migrations.CreateModel(
            name='FlatPageSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Param\xe8tre',
                'verbose_name_plural': 'Param\xe8tres',
            },
        ),
    ]
