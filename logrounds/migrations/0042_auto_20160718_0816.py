# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-18 13:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logrounds', '0041_auto_20160715_1034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='period',
            name='phase',
        ),
        migrations.AddField(
            model_name='period',
            name='phase_days',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='period',
            name='phase_hours',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='period',
            name='phase_min',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='logentry',
            name='log_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 18, 8, 16, 49, 945706), null=True),
        ),
    ]
