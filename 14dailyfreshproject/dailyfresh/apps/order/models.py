# coding:utf8
from django.db import models
from db.base_model import BaseModel

from user.models import User,Address
from goods.models import GoodsSKU
# Create your models here.


class OrderInfo(BaseModel):
    """订单模型类"""
    PAY_METHODS = {
        '1': "货到付款",
        '2': "微信支付",
        '3': "支付宝",
        '4': '银联支付'
    }

    PAY_METHODS_ENUM = {
        "CASH": 1,
        "ALIPAY": 2
    }

    ORDER_STATUS_ENUM = {
        "UNPAID": 1,
        "UNSEND": 2,
        "UNRECEIVED": 3,
        "UNCOMMENT": 4,
        "FINISHED": 5
    }
    PAY_METHOD_CHOICES = (
        (1, '货到付款'),
        (2, '微信支付'),
        (3, '支付宝'),
        (4, '银联支付')
    )

    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成')
    )

    order_id = models.CharField(max_length=128, primary_key=True, verbose_name=u'订单id')
    user = models.ForeignKey(User, verbose_name=u'用户')
    addr = models.ForeignKey(Address, verbose_name=u'地址')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=3, verbose_name=u'支付方式')
    total_count = models.IntegerField(default=1, verbose_name=u'商品数量')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'商品总价')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name=u'订单运费')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name=u'订单状态')
    trade_no = models.CharField(max_length=128, default='',verbose_name=u'支付编号')

    class Meta:
        db_table = 'df_order_info'
        verbose_name = u'订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_id
    
    
class OrderGoods(BaseModel):
    """订单商品模型类"""
    order = models.ForeignKey(OrderInfo, verbose_name=u'订单')
    sku = models.ForeignKey(GoodsSKU, verbose_name=u'商品SKU')
    count = models.IntegerField(default=1, verbose_name=u'商品数目')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'商品价格')
    comment = models.CharField(max_length=256,null=True,blank=True, verbose_name=u'评论')

    class Meta:
        db_table = 'df_order_goods'
        verbose_name = u'订单商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order.order_id