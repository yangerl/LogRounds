# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 19:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogDef',
            fields=[
                ('LogDef_id', models.AutoField(primary_key=True, serialize=False)),
                ('LogDef_name', models.CharField(max_length=20)),
                ('selection_value', models.BooleanField(default=False)),
                ('numeric_value', models.BooleanField(default=True)),
                ('units', models.CharField(max_length=8)),
                ('low_low', models.IntegerField()),
                ('high_high', models.IntegerField()),
                ('low', models.FloatField()),
                ('high', models.FloatField()),
                ('LogDef_desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('Entry_id', models.AutoField(primary_key=True, serialize=False)),
                ('num_value', models.FloatField()),
                ('select_value', models.BooleanField()),
                ('LogDef_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logrounds.LogDef')),
            ],
        ),
        migrations.CreateModel(
            name='LogSet',
            fields=[
                ('LogSet_id', models.AutoField(primary_key=True, serialize=False)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('log_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='RoundType',
            fields=[
                ('rt_id', models.AutoField(primary_key=True, serialize=False)),
                ('rt_name', models.CharField(max_length=50)),
                ('rt_desc', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='logset',
            name='rt_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logrounds.RoundType'),
        ),
        migrations.AddField(
            model_name='logentry',
            name='LogSet_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logrounds.LogSet'),
        ),
        migrations.AddField(
            model_name='logdef',
            name='entry',
            field=models.ManyToManyField(through='logrounds.LogEntry', to='logrounds.LogSet'),
        ),
        migrations.AddField(
            model_name='logdef',
            name='rt_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logrounds.RoundType'),
        ),
    ]