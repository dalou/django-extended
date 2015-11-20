# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_extended', '0006_auto_20151120_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailing',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Cr\xe9\xe9 le'),
        ),
        migrations.AlterField(
            model_name='emailing',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Modifi\xe9 le', db_index=True),
        ),
        migrations.AlterField(
            model_name='emailingtransaction',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Cr\xe9\xe9 le'),
        ),
        migrations.AlterField(
            model_name='emailingtransaction',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Modifi\xe9 le', db_index=True),
        ),
        migrations.AlterField(
            model_name='emailinguseractivationtoken',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Cr\xe9\xe9 le'),
        ),
        migrations.AlterField(
            model_name='emailinguseractivationtoken',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Modifi\xe9 le', db_index=True),
        ),
    ]
