# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailing', '0002_auto_20151111_1104'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AdminEmail',
            new_name='TestEmail',
        ),
    ]
