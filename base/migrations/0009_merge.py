# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-23 06:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_case_case_sort'),
    ]

    operations = [
        migrations.CreateModel(
            name='Merge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cell_range', models.TextField(blank=True, null=True, verbose_name='\u5408\u5e76\u533a\u57df')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Project')),
            ],
        ),
    ]
