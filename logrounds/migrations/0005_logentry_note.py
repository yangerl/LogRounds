# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logrounds', '0004_auto_20160629_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='note',
            field=models.TextField(null=True),
        ),
    ]