from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django_redis import get_redis_connection

from goods.models import GoodsSKU
from utils.mixin import LoginRequiredMixin


# 添加商品到购物车:
# 1）请求方式，采用ajax post
# 如果涉及到数据的修改(新增，更新，删除), 采用post
# 如果只涉及到数据的获取，采用get
# 2) 传递参数: 商品id(sku_id) 商品数量(count)

# /cart/add
class CartAddView(View):
    """添加购物车"""
    def post(self,request):
        # 判断用户是否登录
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res':1,'errmsg':'用户未登录'})

        good_id = request.POST.get('good_id')
        count = int(request.POST.get('count'))

        # 获取商品的库存
        stock = GoodsSKU.objects.get(id=good_id).stock

        # 连接redis
        conn = get_redis_connection('default')
        cart_key = 'cart_%s' %user.id
        # 获取之前用户加入购物车的数量 有就更新 没有就添加
        cart_count = conn.hget(cart_key,good_id)
        if cart_count:
            count += int(cart_count)
        # 判断库存的数量 如果大于库存就不能添加
        if count > stock:
            return JsonResponse({'res': 2, 'errmsg': '库存不足'})
        # 更新购物车数量
        conn.hset(cart_key,good_id,count)

        #获取用户的购物车总条目
        total_count = conn.hlen(cart_key)

        return JsonResponse({'res': 0, 'mssage': '添加成功','total_count':'total_count'})

# /cart/info
class CartInfoView(LoginRequiredMixin,View):
    """我的购物车"""
    def get(self,request):
        user = request.user
        # 连接redis
        conn = get_redis_connection('default')
        # redis hash key
        cart_key = 'cart_%s' %user.id
        # 获取用户的购物车数据
        cart_info = conn.hgetall(cart_key)

        # 商品的总价格和总数量
        total_count = 0
        total_amount = 0
        goods = []
        if cart_info:
            for good_id,count in cart_info.items():
                try:
                    # 商品信息
                    good = GoodsSKU.objects.get(id=good_id)
                    # 单个商品数量
                    count = int(count)
                    # 单个商品总价格
                    amount = count * good.price
                    # 给每个商品动态添加属性
                    good.count = count
                    good.amount = amount
                    goods.append(good)

                    # 计算所有商品的总价格/总数量
                    total_amount += amount
                    total_count += count
                except GoodsSKU.DoesNotExist as e:
                    # 找不到good_id对应的商品，就删除对应的购物车记录
                    conn.hdel(cart_key,good_id) # hdel 删除redis hash key

        context = {'goods':goods,
                   'total_amount':total_amount,
                   'total_count':total_count,}
        return render(request,'cart.html',context)

# /cart/update
class CartUpdateView(View):
    """更新购物车数量"""
    def post(self,request):
        # 判断用户是否登录
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res':1,'errmsg':'用户未登录'})

        good_id = request.POST.get('good_id')
        count = int(request.POST.get('count'))

        # 获取商品的库存
        stock = GoodsSKU.objects.get(id=good_id).stock

        # 连接redis
        conn = get_redis_connection('default')
        cart_key = 'cart_%s' %user.id
        # 判断库存的数量 如果大于库存就不能添加
        if count > stock:
            return JsonResponse({'res': 2, 'errmsg': '库存不足'})
        # 更新购物车数量
        conn.hset(cart_key,good_id,count)

        # 获取用户的购物车总数量
        vals = conn.hvals(cart_key)
        count_vals = 0
        for val in vals:
            count_vals += int(val)

        return JsonResponse({'res': 0, 'mssage': '添加成功','all_count':count_vals})


# /cart/delete
class CartDeleteView(View):
    """删除记录"""
    def post(self,request):
        # 判断用户是否登录
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res':1,'errmsg':'用户未登录'})

        good_id = request.POST.get('good_id')
        # 连接redis
        conn = get_redis_connection('default')
        cart_key = 'cart_%s' %user.id

        conn.hdel(cart_key, good_id)

        # #获取用户的购物车总数量
        vals = conn.hvals(cart_key)
        count_vals = 0
        for val in vals:
            count_vals += int(val)

        return JsonResponse({'res': 0, 'mssage': '删除成功', 'all_count': count_vals})