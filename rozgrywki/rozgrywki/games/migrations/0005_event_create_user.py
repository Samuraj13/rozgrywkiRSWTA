# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-11 13:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0004_auto_20170510_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='create_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
