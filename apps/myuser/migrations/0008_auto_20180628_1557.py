# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-28 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0007_auto_20180628_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailvalirecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '忘记密码'), ('update_email', '修改邮箱')], max_length=50, verbose_name='验证类型'),
        ),
    ]
