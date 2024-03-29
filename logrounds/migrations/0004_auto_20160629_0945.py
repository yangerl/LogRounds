# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 14:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logrounds', '0003_auto_20160629_0752'),
    ]

    operations = [
        migrations.CreateModel(
            name='Selection_value_choices',
            fields=[
                ('svc', models.AutoField(primary_key=True, serialize=False)),
                ('choice_name', models.CharField(max_length=12)),
            ],
        ),
        migrations.RenameField(
            model_name='logdef',
            old_name='has_selection_value',
            new_name='has_qualatative_data',
        ),
        migrations.RemoveField(
            model_name='logdef',
            name='entry',
        ),
        migrations.RemoveField(
            model_name='logdef',
            name='has_numeric_value',
        ),
        migrations.RemoveField(
            model_name='logdef',
            name='selection_value_text',
        ),
        migrations.AlterField(
            model_name='logdef',
            name='units',
            field=models.CharField(max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='logdef',
            name='selection_value',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='logrounds.Selection_value_choices'),
            preserve_default=False,
        ),
    ]
