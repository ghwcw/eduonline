# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-25 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20180625_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='image',
            field=models.ImageField(blank=True, default='org/default-org.jpg', null=True, upload_to='org/%Y/%m', verbose_name='logo'),
        ),
    ]
