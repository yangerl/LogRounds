# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 17:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logrounds', '0029_auto_20160705_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='log_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 5, 12, 17, 12, 405022)),
        ),
    ]
