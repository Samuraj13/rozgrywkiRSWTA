# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-30 17:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_auto_20170524_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(default=0)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.TeamEvent')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.Player')),
            ],
        ),
        migrations.CreateModel(
            name='RedCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(default=0)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.TeamEvent')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Shots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.TeamEvent')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.Player')),
            ],
        ),
        migrations.CreateModel(
            name='YellowCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(default=0)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.TeamEvent')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.Player')),
            ],
        ),
    ]
