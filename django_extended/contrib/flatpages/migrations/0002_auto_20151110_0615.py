# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import fields_bundle.fields.html


class Migration(migrations.Migration):

    dependencies = [
        ('flatpage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flatpage',
            name='content',
            field=fields_bundle.fields.html.HTMLField(verbose_name='Contenu', blank=True),
        ),
    ]
