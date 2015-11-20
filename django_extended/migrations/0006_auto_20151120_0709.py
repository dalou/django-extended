# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('django_extended', '0005_auto_20151119_1209'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailing',
            options={'ordering': ('-created_date',), 'verbose_name': 'Email group\xe9', 'verbose_name_plural': 'Emails group\xe9s'},
        ),
        migrations.AlterModelOptions(
            name='emailingtransaction',
            options={'ordering': ('-created_date',), 'verbose_name': 'Email - Transaction', 'verbose_name_plural': 'Email - Transactions'},
        ),
        migrations.AlterModelOptions(
            name='emailinguseractivationtoken',
            options={'ordering': ('-activation_date',), 'verbose_name': "Cl\xe9 d'activation", 'verbose_name_plural': "Cl\xe9s d'activation"},
        ),
        migrations.RemoveField(
            model_name='emailing',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='emailingtransaction',
            name='date_created',
        ),
        migrations.AddField(
            model_name='emailing',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 20, 6, 9, 43, 257100, tzinfo=utc), verbose_name='Date created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emailing',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 20, 6, 9, 45, 973407, tzinfo=utc), auto_now=True, verbose_name='Date updated', db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emailingtransaction',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 20, 6, 9, 47, 938758, tzinfo=utc), verbose_name='Date created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emailingtransaction',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 20, 6, 9, 50, 802031, tzinfo=utc), auto_now=True, verbose_name='Date updated', db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emailinguseractivationtoken',
            name='activation_date',
            field=models.DateTimeField(null=True, verbose_name="date d'activation", blank=True),
        ),
        migrations.AddField(
            model_name='emailinguseractivationtoken',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 20, 6, 9, 53, 788017, tzinfo=utc), verbose_name='Date created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emailinguseractivationtoken',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 20, 6, 9, 56, 9678, tzinfo=utc), auto_now=True, verbose_name='Date updated', db_index=True),
            preserve_default=False,
        ),
    ]
