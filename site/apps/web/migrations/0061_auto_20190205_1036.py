# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-05 18:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0060_product_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['order'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
    ]
