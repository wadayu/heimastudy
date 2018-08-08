from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel
# Create your models here.


class User(AbstractUser, BaseModel):
    """用户模型类"""
    gender = models.CharField(max_length=6,choices=(('male',u'男'),('female',u'女')),default='male',verbose_name=u'性别')

    class Meta:
        db_table = 'df_user'
        verbose_name = u'用户'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.username


class Address(BaseModel):
    """地址模型类"""
    user = models.ForeignKey(User, verbose_name=u'所属账户')
    receiver = models.CharField(max_length=20, verbose_name=u'收件人')
    addr = models.CharField(max_length=256, verbose_name=u'收件地址')
    zip_code = models.CharField(max_length=6, null=True, verbose_name=u'邮政编码')
    phone = models.CharField(max_length=11, verbose_name=u'联系电话')
    is_default = models.BooleanField(default=False, verbose_name=u'是否默认')

    class Meta:
        db_table = 'df_address'
        verbose_name = u'地址'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return '{0}({1})'.format(self.user, self.addr)
