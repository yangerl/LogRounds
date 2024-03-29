# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logrounds', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logdef',
            old_name='numeric_value',
            new_name='has_numeric_value',
        ),
        migrations.RenameField(
            model_name='logdef',
            old_name='selection_value',
            new_name='has_selection_value',
        ),
        migrations.AddField(
            model_name='logdef',
            name='selection_value_text',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='logdef',
            name='high',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='logdef',
            name='high_high',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='logdef',
            name='low',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='logdef',
            name='low_low',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='num_value',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='select_value',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='logset',
            name='log_time',
            field=models.TimeField(null=True),
        ),
    ]
