#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/8/7 15:49'

import xadmin

from goods.models import GoodsType,Goods,GoodsSKU,GoodsImage,IndexGoodsBanner,IndexTypeGoodsBanner,IndexPromotionBanner
from xadmin.views.base import ModelAdminView, filter_hook, csrf_protect_m

class BaseAdmin(object):
    """当从后台更新数据库时，调用指定的函数"""
    def save_models(self):
        obj = self.new_obj
        obj.save()

        from celery_tasks.tasks import generate_static_index_html
        # 当数据更新的时候重新生成静态页面
        generate_static_index_html.delay()

        from django.core.cache import cache
        # 当数据更新的时候删除缓存
        cache.delete('index_page_data')

    def delete_models(self,*args,**kwargs):
        # *args 返回的一个QuerySet对象
        for obj in args:
            obj.delete()

        from celery_tasks.tasks import generate_static_index_html
        # 当数据更新的时候重新生成静态页面
        generate_static_index_html.delay()

        from django.core.cache import cache
        # 当数据更新的时候删除缓存
        cache.delete('index_page_data')


class GoodsTypeAdmin(BaseAdmin):
    list_display = ['name', 'logo', 'image','create_time','update_time','is_delete']
    search_fields = ['name', 'logo', 'image','create_time','update_time','is_delete']
    list_filter = ['name', 'logo', 'image','create_time','update_time','is_delete']
    model_icon = 'fa fa-cubes'


class GoodsAdmin(BaseAdmin):
    list_display = ['name', 'detail', 'create_time', 'update_time', 'is_delete']
    search_fields = ['name', 'detail', 'create_time', 'update_time', 'is_delete']
    list_filter = ['name', 'detail', 'create_time', 'update_time', 'is_delete']
    style_fields = {'detail': 'ueditor'}
    model_icon = 'fa fa-creative-commons'


class GoodsSKUAdmin(BaseAdmin):
    list_display = ['type', 'goods', 'name', 'desc', 'price','unite','image','stock','sales','status','create_time', 'update_time', 'is_delete']
    search_fields = ['type__name', 'goods__name', 'name', 'desc', 'price','unite','image','stock','sales','status','create_time', 'update_time', 'is_delete']
    list_filter = ['type__name', 'goods__name', 'name', 'desc', 'price','unite','image','stock','sales','status','create_time', 'update_time', 'is_delete']
    list_editable = ['stock', 'desc']
    model_icon = 'fa fa-dashcube'


class GoodsImageAdmin(BaseAdmin):
    list_display = ['sku', 'image', 'create_time', 'update_time', 'is_delete']
    search_fields = ['sku', 'image', 'create_time', 'update_time', 'is_delete']
    list_filter = ['sku__name', 'image', 'create_time', 'update_time', 'is_delete']
    model_icon = 'fa fa-file-image-o'


class IndexGoodsBannerAdmin(BaseAdmin):
    list_display = ['sku', 'image', 'index','create_time','update_time','is_delete']
    search_fields = ['sku', 'image', 'index','create_time','update_time','is_delete']
    list_filter = ['sku__name', 'image', 'index','create_time','update_time','is_delete']


class IndexTypeGoodsBannerAdmin(BaseAdmin):
    list_display = ['type', 'sku', 'display_type','index','create_time','update_time','is_delete']
    search_fields = ['type', 'sku', 'display_type','index','create_time','update_time','is_delete']
    list_filter = ['type__name', 'sku__name', 'display_type','index','create_time','update_time','is_delete']


class IndexPromotionBannerAdmin(BaseAdmin):
    list_display = ['name', 'url', 'image','index','create_time','update_time','is_delete']
    search_fields = ['name', 'url', 'image','index','create_time','update_time','is_delete']
    list_filter = ['name', 'url', 'image','index','create_time','update_time','is_delete']

xadmin.site.register(GoodsType,GoodsTypeAdmin)
xadmin.site.register(Goods,GoodsAdmin)
xadmin.site.register(GoodsSKU,GoodsSKUAdmin)
xadmin.site.register(GoodsImage,GoodsImageAdmin)
xadmin.site.register(IndexGoodsBanner,IndexGoodsBannerAdmin)
xadmin.site.register(IndexTypeGoodsBanner,IndexTypeGoodsBannerAdmin)
xadmin.site.register(IndexPromotionBanner,IndexPromotionBannerAdmin)
