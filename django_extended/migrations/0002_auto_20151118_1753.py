# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_extended', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailing',
            name='template_name',
        ),
        migrations.AddField(
            model_name='emailing',
            name='receivers_test',
            field=models.TextField(null=True, verbose_name='Emails destination de test', blank=True),
        ),
        migrations.AddField(
            model_name='emailing',
            name='sender',
            field=models.EmailField(max_length=254, null=True, verbose_name='Email envoyeur', blank=True),
        ),
        migrations.AlterField(
            model_name='emailing',
            name='receivers',
            field=models.TextField(null=True, verbose_name='Emails destination r\xe9\xe9lles', blank=True),
        ),
        migrations.AlterField(
            model_name='emailing',
            name='template',
            field=models.TextField(verbose_name='Template'),
        ),
    ]
