# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-01 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logrounds', '0056_auto_20160728_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logdef',
            name='desc',
            field=models.TextField(blank=True, null=True),
        ),
    ]