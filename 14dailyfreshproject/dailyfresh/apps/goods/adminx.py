#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/8/7 15:49'

import xadmin

from goods.models import GoodsType,Goods,GoodsSKU,GoodsImage,IndexGoodsBanner,IndexTypeGoodsBanner,IndexPromotionBanner

class GoodsTypeAdmin(object):
    list_display = ['name', 'logo', 'image','create_time','update_time','is_delete']
    search_fields = ['name', 'logo', 'image','create_time','update_time','is_delete']
    list_filter = ['name', 'logo', 'image','create_time','update_time','is_delete']
    model_icon = 'fa fa-cubes'


class GoodsAdmin(object):
    list_display = ['name', 'detail', 'create_time', 'update_time', 'is_delete']
    search_fields = ['name', 'detail', 'create_time', 'update_time', 'is_delete']
    list_filter = ['name', 'detail', 'create_time', 'update_time', 'is_delete']
    style_fields = {'detail': 'ueditor'}
    model_icon = 'fa fa-creative-commons'


class GoodsSKUAdmin(object):
    list_display = ['type', 'goods', 'name', 'desc', 'price','unite','image','stock','sales','status','create_time', 'update_time', 'is_delete']
    search_fields = ['type', 'goods', 'name', 'desc', 'price','unite','image','stock','sales','status','create_time', 'update_time', 'is_delete']
    list_filter = ['type__name', 'goods__name', 'name', 'desc', 'price','unite','image','stock','sales','status','create_time', 'update_time', 'is_delete']
    model_icon = 'fa fa-dashcube'


class GoodsImageAdmin(object):
    list_display = ['sku', 'image', 'create_time', 'update_time', 'is_delete']
    search_fields = ['sku', 'image', 'create_time', 'update_time', 'is_delete']
    list_filter = ['sku__name', 'image', 'create_time', 'update_time', 'is_delete']
    model_icon = 'fa fa-file-image-o'


class IndexGoodsBannerAdmin(object):
    list_display = ['sku', 'image', 'index','create_time','update_time','is_delete']
    search_fields = ['sku', 'image', 'index','create_time','update_time','is_delete']
    list_filter = ['sku__name', 'image', 'index','create_time','update_time','is_delete']


class IndexTypeGoodsBannerAdmin(object):
    list_display = ['type', 'sku', 'display_type','index','create_time','update_time','is_delete']
    search_fields = ['type', 'sku', 'display_type','index','create_time','update_time','is_delete']
    list_filter = ['type__name', 'sku__name', 'display_type','index','create_time','update_time','is_delete']


class IndexPromotionBannerAdmin(object):
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
