# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20180730_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadPic',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('path', models.ImageField(upload_to='books/%Y%m%d/', verbose_name='上传路径')),
            ],
        ),
        migrations.AlterField(
            model_name='areainfo',
            name='pid',
            field=models.ForeignKey(to='books.AreaInfo', null=True, blank=True, verbose_name='父级地区'),
        ),
    ]
