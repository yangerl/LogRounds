# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 14:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logrounds', '0015_auto_20160630_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='log_time',
            field=models.TimeField(default=datetime.time(9, 20, 42, 71519)),
        ),
    ]
