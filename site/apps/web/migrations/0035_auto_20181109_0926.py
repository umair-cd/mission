# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-09 17:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0034_auto_20181109_0916'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homepagecollection',
            options={'ordering': ['order'], 'verbose_name': 'Ready for a quick snack', 'verbose_name_plural': 'Ready for a quick snack'},
        ),
        migrations.AlterUniqueTogether(
            name='homepagecollection',
            unique_together=set([('homepage', 'collection')]),
        ),
    ]
