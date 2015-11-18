# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_extended', '0003_auto_20151118_1806'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailingtransaction',
            old_name='email',
            new_name='emailing',
        ),
        migrations.RemoveField(
            model_name='emailingtransaction',
            name='is_sent',
        ),
        migrations.AddField(
            model_name='emailingtransaction',
            name='send_count',
            field=models.IntegerField(default=0, verbose_name="Compteur d'envois"),
        ),
        migrations.AlterField(
            model_name='emailing',
            name='receivers',
            field=models.TextField(null=True, verbose_name='Vers (destinations r\xe9\xe9lles)', blank=True),
        ),
        migrations.AlterField(
            model_name='emailing',
            name='receivers_test',
            field=models.TextField(null=True, verbose_name='Vers (destination de test)', blank=True),
        ),
        migrations.AlterField(
            model_name='emailing',
            name='sender',
            field=models.CharField(max_length=254, null=True, verbose_name='De', blank=True),
        ),
    ]
