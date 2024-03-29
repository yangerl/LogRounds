# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 19:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag_value', models.IntegerField()),
                ('note', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='FlagTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag_name', models.CharField(max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='LogDef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('desc', models.TextField(blank=True, null=True)),
                ('is_qual_data', models.BooleanField(default=False)),
                ('units', models.CharField(blank=True, max_length=20, null=True)),
                ('low_low', models.FloatField(blank=True, null=True)),
                ('high_high', models.FloatField(blank=True, null=True)),
                ('low', models.FloatField(blank=True, null=True)),
                ('high', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_value', models.FloatField(blank=True, null=True)),
                ('select_value', models.TextField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('log_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('lg_def', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logrounds.LogDef')),
            ],
        ),
        migrations.CreateModel(
            name='LogSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('next_time', models.DateTimeField()),
                ('log_time', models.TimeField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(-1, 'Missed (Partial)'), (0, 'Missed'), (1, 'In Progress'), (2, 'In Progress (Late)'), (3, 'Complete'), (4, 'Complete (Late)')], null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('scale', models.IntegerField(help_text='Time between Sets')),
                ('unit', models.CharField(help_text='Units for the scale (days, hours, or minutes)', max_length=10)),
                ('phase_days', models.IntegerField()),
                ('phase_hours', models.IntegerField()),
                ('phase_min', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RoundType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rt_name', models.CharField(max_length=50)),
                ('rt_desc', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prd', to='logrounds.Period')),
            ],
        ),
        migrations.AddField(
            model_name='logset',
            name='rt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='row', to='logrounds.RoundType'),
        ),
        migrations.AddField(
            model_name='logentry',
            name='lg_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logrounds.LogSet'),
        ),
        migrations.AddField(
            model_name='logentry',
            name='parent',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prev_edit', to='logrounds.LogEntry'),
        ),
        migrations.AddField(
            model_name='logdef',
            name='rt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='col', to='logrounds.RoundType'),
        ),
        migrations.AddField(
            model_name='flags',
            name='flag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flagtype', to='logrounds.FlagTypes'),
        ),
        migrations.AddField(
            model_name='flags',
            name='log_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logentry', to='logrounds.LogEntry'),
        ),
    ]
