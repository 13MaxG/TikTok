# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-22 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='content',
            field=models.TextField(default=''),
        ),
    ]