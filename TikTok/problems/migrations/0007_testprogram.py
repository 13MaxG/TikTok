# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-20 19:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0006_auto_20151218_2157'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(default='')),
                ('time', models.FloatField(default=10.0)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems.Problem')),
            ],
        ),
    ]
