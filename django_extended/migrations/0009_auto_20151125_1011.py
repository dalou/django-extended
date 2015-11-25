# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_extended', '0008_auto_20151120_0906'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmailingTestEmail',
        ),
        migrations.RemoveField(
            model_name='emailingtransaction',
            name='emailing',
        ),
        migrations.DeleteModel(
            name='EmailingUserActivationToken',
        ),
        migrations.RemoveField(
            model_name='flatpage',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='flatpageposition',
            name='flatpage',
        ),
        migrations.DeleteModel(
            name='FlatPageSettings',
        ),
        migrations.DeleteModel(
            name='Emailing',
        ),
        migrations.DeleteModel(
            name='EmailingTransaction',
        ),
        migrations.DeleteModel(
            name='FlatPage',
        ),
        migrations.DeleteModel(
            name='FlatPagePosition',
        ),
    ]
