# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-19 18:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_auto_20161019_1628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='conversion_factor',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='purchasing_unit_of_measure',
        ),
        migrations.AddField(
            model_name='inventory',
            name='purchasing_conversion_factor',
            field=models.CharField(default='1 ea:1 ea', max_length=32, verbose_name='Purchasing Conversion Factor'),
            preserve_default=False,
        ),
    ]