# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-31 19:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogengine', '0008_auto_20160321_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blogengine.Category'),
        ),
    ]
