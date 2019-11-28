# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-12 22:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0038_auto_20181112_0848'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeLandingPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collections_title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RecipePageCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Collection')),
                ('recipe_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.RecipeLandingPage')),
            ],
            options={
                'verbose_name': 'Recipe Page Collections',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='RecipePageHeroCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eyebrow_text', models.CharField(default='Featured Collection', max_length=200)),
                ('cta_text', models.CharField(default='View Recipe Collection', max_length=200)),
                ('order', models.PositiveIntegerField(default=0)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Collection')),
                ('recipe_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.RecipeLandingPage')),
            ],
            options={
                'verbose_name': 'Recipe Page Hero Collections',
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='recipelandingpage',
            name='collections',
            field=models.ManyToManyField(related_name='recipe_page_collections', through='web.RecipePageCollection', to='web.Collection', verbose_name='Recipe Collections'),
        ),
        migrations.AddField(
            model_name='recipelandingpage',
            name='hero_collections',
            field=models.ManyToManyField(related_name='recipe_page_hero_collections', through='web.RecipePageHeroCollection', to='web.Collection', verbose_name='Recipe Hero Collections'),
        ),
        migrations.AlterUniqueTogether(
            name='recipepageherocollection',
            unique_together=set([('recipe_page', 'collection')]),
        ),
        migrations.AlterUniqueTogether(
            name='recipepagecollection',
            unique_together=set([('recipe_page', 'collection')]),
        ),
        migrations.RemoveField(
            model_name='collection',
            name='is_featured_on_landing',
        ),
    ]
