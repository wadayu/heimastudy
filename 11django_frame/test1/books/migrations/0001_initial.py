# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-07-26 10:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='名称')),
                ('pub_data', models.DateField(auto_now_add=True, verbose_name='发布时间')),
                ('reads', models.IntegerField(default=0, verbose_name='阅读量')),
                ('comments', models.IntegerField(default=0, verbose_name='评论数')),
            ],
            options={
                'verbose_name_plural': '书籍名称',
                'verbose_name': '书籍名称',
                'db_table': 'bookinfo',
            },
        ),
        migrations.CreateModel(
            name='HeroInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='名字')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('skill', models.CharField(max_length=20, verbose_name='技能')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.BookInfo', verbose_name='书籍名称')),
            ],
            options={
                'verbose_name_plural': '英雄名称',
                'verbose_name': '英雄名称',
                'db_table': 'heroinfo',
            },
        ),
    ]
