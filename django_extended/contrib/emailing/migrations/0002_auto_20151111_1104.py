# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Adresse email')),
            ],
        ),
        migrations.CreateModel(
            name='UserActivationToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='Adresse email', db_index=True)),
                ('token', models.CharField(unique=True, max_length=64, verbose_name="Token d'activation", db_index=True)),
                ('is_used', models.BooleanField(default=False, verbose_name='Utilis\xe9 ?')),
                ('expiration_date', models.DateTimeField(null=True, verbose_name="date d'expiration", blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='email',
            name='template_name',
            field=models.TextField(null=True, verbose_name='Template name', blank=True),
        ),
    ]
