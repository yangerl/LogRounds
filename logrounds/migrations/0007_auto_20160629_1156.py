# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 16:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logrounds', '0006_auto_20160629_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logdef',
            name='LogDef',
        ),
        migrations.RemoveField(
            model_name='logset',
            name='LogSet',
        ),
        migrations.RemoveField(
            model_name='roundtype',
            name='rt',
        ),
        migrations.RemoveField(
            model_name='selection_value_choices',
            name='svc',
        ),
        migrations.AddField(
            model_name='logdef',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='logset',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roundtype',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='selection_value_choices',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
