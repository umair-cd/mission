# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-07 15:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0029_sprinklruser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['category__title', 'order'], 'verbose_name': 'Question', 'verbose_name_plural': 'FAQ Questions'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='sub_category',
        ),
        migrations.AddField(
            model_name='product',
            name='sub_category',
            field=models.ManyToManyField(related_name='product', to='web.SubCategory'),
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='category',
        ),
        migrations.AddField(
            model_name='subcategory',
            name='category',
            field=models.ManyToManyField(to='web.Category'),
        ),
    ]
