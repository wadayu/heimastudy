from django.conf.urls import url

from cart.views import CartAddView,CartInfoView,CartUpdateView,CartDeleteView

urlpatterns = [
    # 首页
    url(r'^add/$', CartAddView.as_view(), name='cart_add' ), # 购物车添加
    url(r'^info/$', CartInfoView.as_view(), name='cart_show' ), # 购物车显示
    url(r'^update/$', CartUpdateView.as_view(), name='cart_update' ), # 购物车数量更新
    url(r'^delete/$', CartDeleteView.as_view(), name='cart_delete' ), # 购物车商品删除
]
