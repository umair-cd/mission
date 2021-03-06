# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-28 04:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0017_auto_20180826_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='is_featured_on_homepage',
            field=models.BooleanField(default=False, help_text='Check if this recipe should be featured on the homepage'),
            preserve_default=False,
        ),
    ]
