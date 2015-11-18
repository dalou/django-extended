# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailing', '0003_auto_20151116_0936'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Cr\xe9\xe9 le')),
                ('receiver', models.EmailField(max_length=254, verbose_name='Adresse email')),
                ('is_sent', models.BooleanField(default=False, verbose_name='Envoy\xe9 ?')),
            ],
            options={
                'ordering': ('-date_created',),
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.AlterModelOptions(
            name='email',
            options={'ordering': ('-date_created',), 'verbose_name': 'Email group\xe9', 'verbose_name_plural': 'Emails group\xe9s'},
        ),
        migrations.RemoveField(
            model_name='email',
            name='email',
        ),
        migrations.AddField(
            model_name='email',
            name='receivers',
            field=models.TextField(default='', max_length=254, verbose_name='Adresses emails'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emailtransaction',
            name='email',
            field=models.ForeignKey(to='emailing.Email'),
        ),
    ]
