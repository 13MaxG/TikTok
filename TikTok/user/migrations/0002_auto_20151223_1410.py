# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='motto',
            field=models.CharField(blank=True, max_length=140),
        ),
    ]
