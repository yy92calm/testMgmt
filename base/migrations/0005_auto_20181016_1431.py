# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-16 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20181011_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='QC',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='\u8ddf\u8fdb\u4eba'),
        ),
        migrations.AddField(
            model_name='project',
            name='begin_time',
            field=models.TextField(blank=True, max_length=50, null=True, verbose_name='\u63d0\u6d4b\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='project',
            name='end_time',
            field=models.TextField(blank=True, max_length=50, null=True, verbose_name='\u4e0a\u7ebf\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='project',
            name='prj_num',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='JIRA\u5355\u53f7'),
        ),
        migrations.AlterField(
            model_name='project',
            name=b'description',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='\u4e1a\u52a1\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='project',
            name=b'prj_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='JIRA\u5355\u540d'),
        ),
    ]