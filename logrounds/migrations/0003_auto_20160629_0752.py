# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 12:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logrounds', '0002_auto_20160629_0746'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logdef',
            old_name='LogDef_id',
            new_name='LogDef',
        ),
        migrations.RenameField(
            model_name='logdef',
            old_name='rt_id',
            new_name='rt',
        ),
        migrations.RenameField(
            model_name='logentry',
            old_name='Entry_id',
            new_name='Entry',
        ),
        migrations.RenameField(
            model_name='logentry',
            old_name='LogDef_id',
            new_name='LogDef',
        ),
        migrations.RenameField(
            model_name='logentry',
            old_name='LogSet_id',
            new_name='LogSet',
        ),
        migrations.RenameField(
            model_name='logset',
            old_name='LogSet_id',
            new_name='LogSet',
        ),
        migrations.RenameField(
            model_name='logset',
            old_name='rt_id',
            new_name='rt',
        ),
        migrations.RenameField(
            model_name='roundtype',
            old_name='rt_id',
            new_name='rt',
        ),
    ]