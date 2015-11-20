# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_extended', '0007_auto_20151120_0720'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailinguseractivationtoken',
            options={'ordering': ('activation_date',), 'verbose_name': "Cl\xe9 d'activation", 'verbose_name_plural': "Cl\xe9s d'activation"},
        ),
    ]
