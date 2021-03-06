# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-17 13:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('users_total', models.IntegerField(default=0)),
                ('users_did', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems.Problem'),
        ),
    ]
