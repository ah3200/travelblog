# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-11 21:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogengine', '0002_auto_20160311_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='slug',
            field=models.SlugField(default='ok', max_length=40, unique=True),
            preserve_default=False,
        ),
    ]
