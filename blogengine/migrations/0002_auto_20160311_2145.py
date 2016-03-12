# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-11 21:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogengine', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AddField(
            model_name='story',
            name='slug',
            field=models.SlugField(max_length=40, null=True),
        ),
    ]
