# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-09 16:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0032_auto_20181108_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='eyebrow_title_influencer',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='homepage',
            name='eyebrow_title_product',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='homepage',
            name='eyebrow_title_recipe',
            field=models.CharField(default='', max_length=100),
        ),
    ]
