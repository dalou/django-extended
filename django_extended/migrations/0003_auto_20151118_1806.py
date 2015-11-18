# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_extended', '0002_auto_20151118_1753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailing',
            name='is_sent',
        ),
        migrations.AddField(
            model_name='emailing',
            name='send_count',
            field=models.IntegerField(default=0, verbose_name="Compteur d'envois"),
        ),
        migrations.AddField(
            model_name='emailing',
            name='test_count',
            field=models.IntegerField(default=0, verbose_name='Compteur de tests'),
        ),
    ]
