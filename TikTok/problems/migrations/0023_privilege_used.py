# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-10 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0022_auto_20160210_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='privilege',
            name='used',
            field=models.BooleanField(default=False),
        ),
    ]
