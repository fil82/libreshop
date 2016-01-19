# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-18 20:43
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_description'),
        ('orders', '0002_auto_20151111_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaxRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('state', models.CharField(blank=True, max_length=4, null=True)),
                ('district', models.CharField(blank=True, max_length=4, null=True)),
                ('county', models.CharField(blank=True, max_length=4, null=True)),
                ('city', models.CharField(blank=True, max_length=4, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=16, null=True)),
                ('state_tax_rate', models.DecimalField(decimal_places=4, default=Decimal('0.00'), max_digits=5)),
                ('district_tax_rate', models.DecimalField(decimal_places=4, default=Decimal('0.00'), max_digits=5)),
                ('county_tax_rate', models.DecimalField(decimal_places=4, default=Decimal('0.00'), max_digits=5)),
                ('local_tax_rate', models.DecimalField(decimal_places=4, default=Decimal('0.00'), max_digits=5)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='order',
            name='sales_tax',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8),
        ),
        migrations.AddField(
            model_name='order',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8),
        ),
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8),
        ),
        migrations.AddField(
            model_name='purchase',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Order'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
    ]
