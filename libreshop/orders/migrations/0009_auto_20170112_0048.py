# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-12 00:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20170110_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cost_of_goods_sold',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]
