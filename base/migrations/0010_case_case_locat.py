# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-24 04:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='case_locat',
            field=models.TextField(blank=True, null=True, verbose_name='\u6a21\u5757'),
        ),
    ]
