# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-24 22:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0049_auto_20181121_0130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='video_id',
        ),
        migrations.AddField(
            model_name='recipe',
            name='video_image',
            field=models.ImageField(blank=True, help_text='Poster image for video. If empty, you tube defaul image is used', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='sustainabilitypage',
            name='video_image',
            field=models.ImageField(blank=True, help_text='Poster image for video. If empty, you tube defaul image is used', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='sustainabilitypage',
            name='video_id',
            field=models.CharField(blank=True, help_text='Video ID for video, e.g. https://www.youtube.com/watch?v=7NONdwbqRV8, id would be 7NONdwbqRV8', max_length=255, null=True),
        ),
    ]
