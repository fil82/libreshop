# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-18 23:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20160118_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='token',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
