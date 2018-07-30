# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_aerainfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('atitle', models.CharField(verbose_name='地区名称', max_length=20)),
                ('pid', models.ForeignKey(to='books.AreaInfo', blank=True, null=True)),
            ],
            options={
                'verbose_name': '地区名称',
                'verbose_name_plural': '地区名称',
                'db_table': 'areainfo',
            },
        ),
        migrations.RemoveField(
            model_name='aerainfo',
            name='pid',
        ),
        migrations.DeleteModel(
            name='AeraInfo',
        ),
    ]
