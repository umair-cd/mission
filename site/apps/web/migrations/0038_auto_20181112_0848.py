# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-12 16:48
from __future__ import unicode_literals

import apps.web.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0037_productpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='here_to_make_text',
            field=models.CharField(blank=True, default="I'm here to make ", max_length=100),
        ),
        migrations.AddField(
            model_name='homepage',
            name='social_headline',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='homepage',
            name='social_intro_text',
            field=apps.web.fields.CharFieldWithTextarea(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='collections',
            field=models.ManyToManyField(through='web.HomepageCollection', to='web.Collection', verbose_name='Here to Make Collections'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='eyebrow_title_influencer',
            field=models.CharField(default='', max_length=100, verbose_name='Featured Influencer Eyebrow Title'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='eyebrow_title_product',
            field=models.CharField(default='', max_length=100, verbose_name='Featured Product Eyebrow Title'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='eyebrow_title_recipe',
            field=models.CharField(default='', max_length=100, verbose_name='Featured Recipe Eyebrow Title'),
        ),
    ]
