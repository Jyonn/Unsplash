# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-16 02:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('access_token', models.CharField(max_length=64)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
            ],
        ),
    ]