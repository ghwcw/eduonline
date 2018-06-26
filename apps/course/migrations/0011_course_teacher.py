# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-25 16:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0012_auto_20180625_1554'),
        ('course', '0010_video_howlong'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='organization.Teacher', verbose_name='课程教师'),
        ),
    ]