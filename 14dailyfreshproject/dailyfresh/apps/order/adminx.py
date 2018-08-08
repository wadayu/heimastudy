#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/8/7 15:49'

import xadmin

from order.models import OrderInfo,OrderGoods

class OrderInfoAdimin(object):
    list_display = ['order_id','user','addr','pay_method','total_count','total_price','transit_price','order_status','trade_no','create_time','update_time','is_delete']
    search_fields = ['order_id','user','addr','pay_method','total_count','total_price','transit_price','order_status','trade_no','create_time','update_time','is_delete']
    list_filter = ['order_id','user__username','addr__addr','pay_method','total_count','total_price','transit_price','order_status','trade_no','create_time','update_time','is_delete']
    model_icon= 'fa fa-file-text-o'

class OrderGoodsAdmin(object):
    list_display = ['order', 'sku', 'count', 'price','comment','create_time','update_time','is_delete']
    search_fields = ['order', 'sku', 'count', 'price','comment','create_time','update_time','is_delete']
    list_filter = ['order', 'sku__name', 'count', 'price','comment','create_time','update_time','is_delete']
    model_icon = 'fa fa-list'

xadmin.site.register(OrderInfo,OrderInfoAdimin)
xadmin.site.register(OrderGoods,OrderGoodsAdmin)
