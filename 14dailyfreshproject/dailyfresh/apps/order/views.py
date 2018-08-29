from django.shortcuts import render,redirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.http import JsonResponse,HttpResponse
from django_redis import get_redis_connection
from django.db import transaction
from django.conf import settings

import time,random,os
from alipay import AliPay

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

            order.total_price = total_price + transit_price
            order.total_count = total_count
            order.save()

            transaction.savepoint_commit(sid) # 提交事务
        except Exception as e:
            transaction.savepoint_rollback(sid)
            return JsonResponse({'res': 7, 'errmsg': '下单失败'})

        # 清除购买购物车商品
        conn.hdel(cart_key,*good_ids)
        return JsonResponse({'res': 0, 'errmsg': '订单创建成功'})


# ajax post
# 前端传递的参数:订单id(order_id)
# /order/pay
class OrderPayView(View):
    '''订单支付'''
    def post(self, request):
        '''订单支付'''
        # 用户是否登录
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res':0, 'errmsg':'用户未登录'})

        # 接收参数
        order_id = request.POST.get('order_id')

        # 校验参数
        if not order_id:
            return JsonResponse({'res':1, 'errmsg':'无效的订单id'})

        try:
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=user,
                                          pay_method=3,
                                          order_status=1)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res':2, 'errmsg':'订单错误'})

        # 业务处理:使用python sdk调用支付宝的支付接口
        # 初始化
        alipay = AliPay(
            appid="2016091800536571", # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(settings.BASE_DIR, 'apps/order/app_private_key.pem'),
            alipay_public_key_path=os.path.join(settings.BASE_DIR, 'apps/order/alipay_public_key.pem'), # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )

        # 调用支付接口
        # 电脑网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
        total_pay = order.total_price # Decimal 不可转换json
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id, # 订单id
            total_amount=str(total_pay), # 支付总金额
            subject='天天生鲜付款%s'%order_id,
            return_url=None,
            notify_url=None  # 可选, 不填则使用默认notify url
        )

        # 返回应答
        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
        return JsonResponse({'res':3, 'pay_url':pay_url})

# ajax post
# 前端传递的参数:订单id(order_id)
# /order/check
class CheckPayView(View):
    '''查看订单支付的结果'''
    def post(self, request):
        '''查询支付结果'''
        # 用户是否登录
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})

        # 接收参数
        order_id = request.POST.get('order_id')

        # 校验参数
        if not order_id:
            return JsonResponse({'res': 1, 'errmsg': '无效的订单id'})

        try:
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=user,
                                          pay_method=3,
                                          order_status=1)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '订单错误'})

        # 业务处理:使用python sdk调用支付宝的支付接口
        # 初始化
        alipay = AliPay(
            appid="2016091800536571",  # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(settings.BASE_DIR, 'apps/order/app_private_key.pem'),
            alipay_public_key_path=os.path.join(settings.BASE_DIR, 'apps/order/alipay_public_key.pem'),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )

        # 调用支付宝的交易查询接口
        while True:
            response = alipay.api_alipay_trade_query(order_id)

            # response = {
            #         "trade_no": "2017032121001004070200176844", # 支付宝交易号
            #         "code": "10000", # 接口调用是否成功
            #         "invoice_amount": "20.00",
            #         "open_id": "20880072506750308812798160715407",
            #         "fund_bill_list": [
            #             {
            #                 "amount": "20.00",
            #                 "fund_channel": "ALIPAYACCOUNT"
            #             }
            #         ],
            #         "buyer_logon_id": "csq***@sandbox.com",
            #         "send_pay_date": "2017-03-21 13:29:17",
            #         "receipt_amount": "20.00",
            #         "out_trade_no": "out_trade_no15",
            #         "buyer_pay_amount": "20.00",
            #         "buyer_user_id": "2088102169481075",
            #         "msg": "Success",
            #         "point_amount": "0.00",
            #         "trade_status": "TRADE_SUCCESS", # 支付结果
            #         "total_amount": "20.00"
            # }

            code = response.get('code')

            if code == '10000' and response.get('trade_status') == 'TRADE_SUCCESS':
                # 支付成功
                # 获取支付宝交易号
                trade_no = response.get('trade_no')
                # 更新订单状态
                order.trade_no = trade_no
                order.order_status = 4 # 待评价
                order.save()
                # 返回结果
                return JsonResponse({'res':3, 'message':'支付成功'})
            elif code == '40004' or (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
                # 等待买家付款
                # 业务处理失败，可能一会就会成功
                import time
                time.sleep(5)
                continue
            else:
                # 支付出错
                print(code)
                return JsonResponse({'res':4, 'errmsg':'支付失败'})


class OrderCommentView(LoginRequiredMixin,View):
    def get(self,request,order_id):
        if not order_id:
            return redirect(reverse('user:order'))

        try:
            order = OrderInfo.objects.get(order_id=order_id,user=request.user)
        except Exception as e:
            return redirect(reverse('user:order'))

        all_goods = OrderGoods.objects.filter(order=order)
        order_status = {1: '待支付', 2: '待发货', 3: '待收货', 4: '待评价', 5: '已完成'}

        for good in all_goods:
            amount = good.price * good.count
            good.amount = amount
        order.all_goods =  all_goods
        order.status = order_status.get(order.order_status)
        return render(request,'order_comment.html',{'order':order})

    def post(self,request,order_id):
        if not order_id:
            return redirect(reverse('user:order'))

        try:
            order = OrderInfo.objects.get(order_id=order_id, user=request.user)
        except Exception as e:
            return redirect(reverse('user:order'))

        comment_count = int(request.POST.get('total_count'))

        for i in range(1,comment_count+1):
            good_id = request.POST.get('sku_%s' %i)
            comment = request.POST.get('content_%s' %i)

            try:
                good = OrderGoods.objects.get(order=order,sku_id=good_id)
            except Exception as e:
                continue
            good.comment = comment
            good.save()

        order.order_status = 5
        order.save()

        return redirect(reverse('user:comment'))


