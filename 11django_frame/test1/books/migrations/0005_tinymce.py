# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20180730_1655'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tinymce',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('text', tinymce.models.HTMLField(verbose_name='详情')),
            ],
            options={
                'verbose_name': '富文本编辑器',
            },
        ),
    ]
