# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-29 04:27
from __future__ import unicode_literals

from django.db import migrations
import pyuploadcare.dj.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0018_recipe_is_featured_on_homepage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='marquee_image',
        ),
        migrations.AddField(
            model_name='category',
            name='marquee_image',
            field=pyuploadcare.dj.models.ImageField(blank=True, help_text='Marquee Image for Category page', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='nutritional_facts',
            field=pyuploadcare.dj.models.ImageField(blank=True, help_text='Used to display nutritional facts label', null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='nutritional_facts',
            field=pyuploadcare.dj.models.ImageField(blank=True, help_text='Used to display nutritional facts label', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=pyuploadcare.dj.models.ImageField(blank=True, help_text='Primary product image used on detail and landing pages', null=True),
        ),
    ]
