from django.shortcuts import render,redirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django_redis import get_redis_connection
from django.db import transaction

import time,random

from user.models import Address
from goods.models import GoodsSKU
from order.models import OrderInfo,OrderGoods
from utils.mixin import LoginRequiredMixin


# /order/place
class OrderPlaceView(LoginRequiredMixin,View):
    """订单提交页面"""
    def post(self,request):
        # 获取多个good_id的value值 以[2,3,4]列表的形式展示
        good_ids = request.POST.getlist('good_id')
        if not good_ids:
            return redirect(reverse('cart:cart_show'))
        user = request.user
        cart_key = 'cart_%s' %user.id

        conn = get_redis_connection('default')
        all_goods = []
        total_count = 0
        total_amount = 0
        for good_id in good_ids:
            good = GoodsSKU.objects.get(id=good_id)
            # 获取购物车对应商品的数量
            count = int(conn.hget(cart_key,good_id))
            amount = good.price * count
            # 动态的添加商品数量、小计
            good.count = count
            good.amount = amount

            # 计算商品的总价格 总数量
            total_count += count
            total_amount += amount

            all_goods.append(good)
        # 获取用户的收件地址
        all_addr = Address.objects.filter(user=user)

        # 运费
        freight = 10
        # 实付款
        total_pay = total_amount + freight
        # 商品的id
        all_good_ids = ','.join(good_ids) # '3,4,5,6'
        context = {
            'all_goods':all_goods,
            'total_count':total_count,
            'total_amount':total_amount,
            'all_addr':all_addr,
            'freight':freight,
            'total_pay':total_pay,
            'all_good_ids':all_good_ids
        }
        return render(request,'place_order.html',context)

class OrderCommitView(View):
    """订单的创建"""
    @transaction.atomic()
    def post(self,request):
        # 校验用户是否登录
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res':1,'errmsg':'用户未登录'})

        add_id = request.POST.get('add_id','')
        pay_method = request.POST.get('pay_method','')
        good_ids = request.POST.get('good_ids','')

        # 校验数据是否为空
        if not all([add_id,pay_method,good_ids]):
            return JsonResponse({'res':2,'errmsg':'数据不完整'})

        # 校验地址是否有误
        try:
            addr = Address.objects.get(id=add_id)
        except Exception as e:
            return JsonResponse({'res': 3, 'errmsg': '收件地址有误'})

        # 支付方式校验
        if pay_method not in OrderInfo.PAY_METHODS.keys():
            return JsonResponse({'res': 4, 'errmsg': '支付方式有误'})

        # order_id编号随机数
        order_num = ''
        for i in range(8):
            n = random.randint(0, 9)
            order_num += str(n)

        # 组织数据库参数
        order_id = time.strftime('%Y%m%d%H%M%S') + order_num
        total_count = 0 # 总数量
        total_price = 0 # 总价格
        transit_price = 10  # 运费

        # 设置事务保存点
        sid = transaction.savepoint()
        try:
            # 创建订单表
            order = OrderInfo.objects.create(order_id=order_id,
                                     user=user,
                                     addr=addr,
                                     pay_method=pay_method,
                                     total_count=total_count,
                                     total_price=total_price,
                                     transit_price=transit_price)

            conn = get_redis_connection('default')
            cart_key = 'cart_%s' %user.id
            good_ids = good_ids.split(',') # ['2','3','4']

            for good_id in good_ids:
                try:
                    # select * from df_goods_sku where id=sku_id for update; 悲观锁 查询之前先锁住
                    good = GoodsSKU.objects.select_for_update().get(id=good_id)
                except GoodsSKU.DoesNotExist as e:
                    transaction.savepoint_rollback(sid)  # 商品出现问题是回滚事务
                    return JsonResponse({'res': 5, 'errmsg': '商品不存在'})

                count = int(conn.hget(cart_key,good_id)) # 获取商品订单的数量
                amount = count * good.price  # 商品总价格

                if count > good.stock:
                    transaction.savepoint_rollback(sid)
                    return JsonResponse({'res': 6, 'errmsg': '库存不足'})
                # 将每个商品的订单信息写入到表中
                OrderGoods.objects.create(order=order,
                                          sku=good,
                                          count=count,
                                          price=good.price)

                # 订单数量、价格累计
                total_count += count
                total_price += amount

                # 更新库存的数量和销量
                good.stock -= count
                good.sales += count
                good.save()

            order.total_price = total_price
            order.total_count = total_count
            order.save()

            transaction.savepoint_commit(sid) # 提交事务
        except Exception as e:
            transaction.savepoint_rollback(sid)
            return JsonResponse({'res': 7, 'errmsg': '下单失败'})

        # 清除购买购物车商品
        conn.hdel(cart_key,*good_ids)
        return JsonResponse({'res': 0, 'errmsg': '订单创建成功'})


