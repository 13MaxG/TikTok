# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-28 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submits', '0004_auto_20151222_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submit',
            name='code',
            field=models.TextField(max_length=3),
        ),
    ]
