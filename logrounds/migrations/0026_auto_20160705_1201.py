# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 17:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logrounds', '0025_auto_20160705_1040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flags',
            old_name='flag_id',
            new_name='flag',
        ),
        migrations.RenameField(
            model_name='flags',
            old_name='log_entry_id',
            new_name='log_entry',
        ),
        migrations.RemoveField(
            model_name='flags',
            name='flag_name',
        ),
        migrations.AddField(
            model_name='flags',
            name='flag_value',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flagtypes',
            name='flag_name',
            field=models.CharField(default='default', max_length=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='logentry',
            name='log_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 5, 12, 1, 11, 509127)),
        ),
    ]
