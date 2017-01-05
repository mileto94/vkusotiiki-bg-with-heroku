# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-27 23:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0007_auto_20161217_1529'),
        ('recipes', '0009_auto_20161218_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='img', to='filer.Image')),
            ],
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='img',
        ),
        migrations.AddField(
            model_name='recipeimage',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe'),
        ),
    ]