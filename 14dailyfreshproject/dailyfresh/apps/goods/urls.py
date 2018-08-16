from django.conf.urls import url

from goods.views import IndexView,DetailView

urlpatterns = [
    # 首页
    url(r'^$', IndexView.as_view(), name='index' ), # 首页
    url(r'^detail/(?P<goods_id>\d+)/$', DetailView.as_view(), name='detail' ), # 商品详情页
]
