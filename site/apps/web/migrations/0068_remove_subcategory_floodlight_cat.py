# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-14 03:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0067_category_floodlight_cat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='floodlight_cat',
        ),
    ]
