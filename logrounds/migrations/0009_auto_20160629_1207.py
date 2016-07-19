# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 17:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logrounds', '0008_auto_20160629_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='LogDef',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='yVal', to='logrounds.LogDef'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='LogSet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xVal', to='logrounds.LogSet'),
        ),
    ]
