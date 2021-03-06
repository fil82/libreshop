# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-02 05:03
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_supply'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('number', models.CharField(max_length=64, unique=True, verbose_name='Purchase Order (PO) Number')),
                ('subtotal', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('sales_tax', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('shipping_cost', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8)),
                ('total', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8)),
                ('submitted', models.DateTimeField(default=django.utils.timezone.now)),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Warehouse')),
            ],
            options={
                'verbose_name_plural': 'Purchase Orders',
                'verbose_name': 'Purchase Order',
            },
        ),
        migrations.RemoveField(
            model_name='supply',
            name='inventory',
        ),
        migrations.AddField(
            model_name='supply',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8),
        ),
        migrations.AddField(
            model_name='supply',
            name='name',
            field=models.CharField(default='', max_length=64, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='supply',
            name='receipt_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='supply',
            name='purchase_order',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='inventory.PurchaseOrder'),
            preserve_default=False,
        ),
    ]
