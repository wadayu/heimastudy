# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-08-16 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20180816_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='comment',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='评论'),
        ),
    ]
