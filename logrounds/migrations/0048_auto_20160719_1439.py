# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-19 14:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('logrounds', '0047_auto_20160718_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='log_time',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]
