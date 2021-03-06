# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-11 22:24
from __future__ import unicode_literals

from django.db import migrations, models
import pyuploadcare.dj.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomeCarousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='First line of title', max_length=200, null=True)),
                ('sub_title', models.CharField(blank=True, help_text='Second line of title', max_length=200, null=True)),
                ('background_image', pyuploadcare.dj.models.ImageField(blank=True, help_text='Background image of carousel slide', null=True)),
                ('cta_text', models.CharField(blank=True, default='Explore Recipes', max_length=200, null=True)),
                ('cta_url', models.CharField(blank=True, default='/recipes', max_length=200, null=True)),
            ],
        ),
    ]
