# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AeraInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('atitle', models.CharField(max_length=20, verbose_name='地区名称')),
                ('pid', models.ForeignKey(blank=True, to='books.AeraInfo', null=True)),
            ],
            options={
                'verbose_name': '地区名称',
                'db_table': 'aerainfo',
                'verbose_name_plural': '地区名称',
            },
        ),
    ]
