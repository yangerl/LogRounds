# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-13 15:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logrounds', '0037_auto_20160713_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='logset',
            name='missed',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='logentry',
            name='log_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 13, 10, 31, 0, 568746)),
        ),
    ]
