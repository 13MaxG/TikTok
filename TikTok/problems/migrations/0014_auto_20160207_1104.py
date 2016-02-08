# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-07 10:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0013_group_pub_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='id',
        ),
        migrations.AlterField(
            model_name='group',
            name='shortname',
            field=models.CharField(default='', max_length=255, primary_key=True, serialize=False),
        ),
    ]
