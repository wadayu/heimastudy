from django.db import models
from tinymce.models import HTMLField #富文本编辑器

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

class AreaInfo(models.Model):
    atitle = models.CharField(max_length=20,verbose_name=u'地区名称')
    pid = models.ForeignKey('self',null=True,blank=True,verbose_name=u'父级地区')

    class Meta:
        verbose_name = u'地区名称'
        verbose_name_plural= verbose_name
        db_table = 'areainfo'

    def __str__(self):
        return self.atitle

    def parent(self):
        if self.pid is None:
            return ''
        return self.pid.atitle
    parent.short_description = u'父级地区'
    parent.admin_order_field = 'atitle' # 排序
    

class UploadPic(models.Model):
    path = models.ImageField(upload_to='books/%Y%m%d/',verbose_name=u'上传路径')


class Tinymce(models.Model):
    text = HTMLField(verbose_name='详情')

    class Meta:
        verbose_name = '富文本编辑器'