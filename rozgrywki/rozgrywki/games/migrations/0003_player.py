# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-28 09:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20170428_1033'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_name', models.CharField(max_length=20)),
                ('player_surname', models.CharField(max_length=30)),
                ('team_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.Team')),
            ],
        ),
    ]
