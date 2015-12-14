# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_extended', '0008_auto_20151120_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailing',
            name='sending_range',
            field=models.CharField(default=100, help_text="Les tranches d'envois permette de soulager le serveur d'envoi de masse.", max_length=254, verbose_name="Tranche d'envois maximum par session", choices=[(20, 20), (50, 50), (70, 70), (100, 100)]),
        ),
    ]
