# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-16 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_case_project'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CaseType',
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='\u5f53\u524d\u72b6\u6001'),
        ),
    ]
