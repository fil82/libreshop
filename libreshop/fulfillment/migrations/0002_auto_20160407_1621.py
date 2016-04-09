# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-07 16:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fulfillment', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fulfillmentsettingvalue',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Variant'),
        ),
        migrations.AddField(
            model_name='fulfillmentsetting',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fulfillment.Supplier'),
        ),
        migrations.AddField(
            model_name='fulfillmentpurchase',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fulfillment.FulfillmentOrder'),
        ),
    ]