# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-20 19:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logrounds', '0051_flags_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logset',
            name='status',
            field=models.IntegerField(choices=[(-1, 'Missed (Partial)'), (0, 'Missed'), (1, 'In Progress'), (2, 'In Progress (Late)'), (3, 'Complete'), (4, 'Complete (Late)')], null=True),
        ),
    ]
