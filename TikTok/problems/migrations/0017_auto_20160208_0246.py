# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-08 01:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0016_ranking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ranking',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
