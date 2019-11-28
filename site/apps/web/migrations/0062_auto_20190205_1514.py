# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-05 23:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0061_auto_20190205_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='historypage',
            name='category',
            field=models.CharField(choices=[('none', '-'), ('us', 'US'), ('world', 'World')], default='none', max_length=100),
        ),
        migrations.AddField(
            model_name='historypage',
            name='location',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
