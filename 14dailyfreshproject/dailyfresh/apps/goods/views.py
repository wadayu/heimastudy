from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import View
from django_redis import get_redis_connection
from django.core.cache import cache


from goods.models import IndexGoodsBanner,GoodsType,IndexPromotionBanner,GoodsSKU,GoodsType
from order.models import OrderGoods

# /index
class IndexView(View):
    def get(self,request):
        # 尝试从缓存里获取数据，如果有读取数据
        context = cache.get('index_page_data')
        if context is None:
            print ('设置缓存')
            # 所有的商品类型
            all_types = GoodsType.objects.all()
            # 所有的轮播图片
            all_banners = IndexGoodsBanner.objects.all().order_by('index')
            # 所有的活动展示图
            all_promotionbanners=IndexPromotionBanner.objects.all().order_by('index')
            # 循环商品的种类
            for type in all_types:
                # 获取每个种类的前四个商品
                all_goods = GoodsSKU.objects.filter(type=type)[:4]
                # 动态给type增加属性
                type.all_goods = all_goods

            # 购物车的默认的列表数量


            context = {
                'all_types': all_types,
                'all_banners': all_banners,
                'all_promotionbanners': all_promotionbanners,
            }

            # 设置缓存（setting里设置CACHES选项）
            cache.set('index_page_data',context,3600)

        user = request.user
        cart_count = 0
        if user.is_authenticated():
            # 判断用户是否登录  此处用的redis hash
            con = get_redis_connection('default')
            cart_key = 'cart_%s' %user.id
            cart_count = con.hlen(cart_key)

        # 更新用户的购物车数量
        context.update(cart_count=cart_count)

        return render(request,'index.html',context)


# /detail/\d+
class DetailView(View):
    # 商品详情
    def get(self,request,goods_id):
        try:
            goods = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist as e:
            return redirect(reverse('goods:index'))
        # 所有类型
        all_types = GoodsType.objects.all()
        # 同类新品
        new_goods = GoodsSKU.objects.filter(type=goods.type).order_by('-create_time')[:2]
        # 商品的所有评论
        all_comments = OrderGoods.objects.filter(sku=goods).exclude(comment='')
        # 购物车数量
        user = request.user
        cart_count = 0
        if user.is_authenticated():
            # 判断用户是否登录  此处用的redis hash
            con = get_redis_connection('default')
            cart_key = 'cart_%s' %user.id
            cart_count = con.hlen(cart_key)

        context = {
            'goods':goods,
            'all_types':all_types,
            'new_goods':new_goods,
            'cart_count':cart_count,
            'all_comments':all_comments,
        }
        return render(request,'detail.html',context)