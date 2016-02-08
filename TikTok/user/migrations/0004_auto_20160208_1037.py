# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-08 09:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_ranking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ranking',
            name='user',
        ),
        migrations.AddField(
            model_name='ranking',
            name='my_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.MyUser'),
        ),
    ]