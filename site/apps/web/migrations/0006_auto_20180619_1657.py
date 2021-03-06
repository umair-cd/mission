# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-19 23:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20180619_1627'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['order'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='homecarousel',
            options={'ordering': ['order'], 'verbose_name': 'Home Carousel', 'verbose_name_plural': 'Home Carousel Slides'},
        ),
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='homecarousel',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
