# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 19:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logrounds', '0012_logset_log_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logset',
            name='log_date',
            field=models.DateField(),
        ),
    ]