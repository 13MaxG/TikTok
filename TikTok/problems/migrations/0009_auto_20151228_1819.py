# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-28 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0008_remove_problem_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=5000),
        ),
    ]
