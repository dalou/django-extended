# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailing', '0004_auto_20151116_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='title',
        ),
        migrations.AddField(
            model_name='email',
            name='subject',
            field=models.CharField(max_length=254, null=True, verbose_name='Sujet du mail', blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='receivers',
            field=models.TextField(null=True, verbose_name='Adresses emails', blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='template',
            field=models.TextField(verbose_name='Template du mail'),
        ),
    ]
