# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-12 21:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0058_auto_20181205_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='upc_code',
            field=models.CharField(blank=True, help_text='UPC Code', max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='fraction',
            field=models.CharField(blank=True, choices=[('eigth', '1/8'), ('quarter', '1/4'), ('third', '1/3'), ('half', '1/2'), ('two-thirds', '2/3'), ('three-quarters', '3/4')], max_length=100, null=True),
        ),
    ]
