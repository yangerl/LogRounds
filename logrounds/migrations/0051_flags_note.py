# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-20 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logrounds', '0050_auto_20160720_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='flags',
            name='note',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]