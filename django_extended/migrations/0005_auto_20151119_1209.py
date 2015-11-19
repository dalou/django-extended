# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_extended', '0004_auto_20151118_2134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailingtransaction',
            options={'ordering': ('-date_created',), 'verbose_name': 'Email - Transaction', 'verbose_name_plural': 'Email - Transactions'},
        ),
    ]
