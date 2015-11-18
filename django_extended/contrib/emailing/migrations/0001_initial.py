# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Cr\xe9\xe9 le')),
                ('name', models.CharField(max_length=254, verbose_name='Nom')),
                ('email', models.EmailField(max_length=254, verbose_name='Adresse email')),
                ('title', models.CharField(max_length=254, null=True, verbose_name='Title', blank=True)),
                ('template', models.TextField(verbose_name='Template')),
                ('is_sent', models.BooleanField(default=False, verbose_name='Envoy\xe9 ?')),
            ],
            options={
                'ordering': ('-date_created',),
                'verbose_name': 'Email',
                'verbose_name_plural': 'Emails',
            },
        ),
    ]
