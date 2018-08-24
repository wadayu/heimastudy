from django.conf.urls import  url

from order.views import OrderPlaceView,OrderCommitView
urlpatterns = [
    # 首页
    url(r'^place/$', OrderPlaceView.as_view(), name='place' ), # 订单提交
    url(r'^commit/$', OrderCommitView.as_view(), name='commit' ), # 订单创建
]
