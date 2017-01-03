# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-17 21:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_remove_recipe_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='recipes.Recipe'),
        ),
    ]
