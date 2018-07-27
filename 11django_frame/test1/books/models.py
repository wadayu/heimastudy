from django.db import models

# Create your models here.
from datetime import date,datetime

class BookInfo(models.Model):
    title = models.CharField(max_length=20,verbose_name=u'名称')
    pub_data = models.DateField(auto_now_add=True,verbose_name=u'发布时间')
    reads = models.IntegerField(default=0,verbose_name=u'阅读量')
    comments = models.IntegerField(default=0,verbose_name=u'评论数')
    # add_time = models.DateTimeField(default=datetime.now,verbose_name='创建时间')

    class Meta:
        verbose_name = u'书籍名称'
        verbose_name_plural = verbose_name
        db_table = 'bookinfo'

    def __str__(self):
        return self.title


class HeroInfo(models.Model):
    name = models.CharField(max_length=20,verbose_name=u'名字')
    age = models.IntegerField(verbose_name=u'年龄')
    skill = models.CharField(max_length=20,verbose_name=u'技能')
    book = models.ForeignKey('BookInfo',verbose_name=u'书籍名称')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'创建时间')

    class Meta:
        verbose_name = u'英雄名称'
        verbose_name_plural = verbose_name
        db_table = 'heroinfo'


    def __str__(self):
        return  self.name