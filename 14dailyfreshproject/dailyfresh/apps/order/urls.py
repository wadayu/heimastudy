from django.conf.urls import  url

from order.views import OrderPlaceView,OrderCommitView,OrderPayView,CheckPayView,OrderCommentView
urlpatterns = [
    # 首页
    url(r'^place/$', OrderPlaceView.as_view(), name='place' ), # 订单提交
    url(r'^commit/$', OrderCommitView.as_view(), name='commit' ), # 订单创建
    url(r'^pay/$', OrderPayView.as_view(), name='pay' ), # 订单付款
    url(r'^check/$', CheckPayView.as_view(), name='check'),  # 查询支付交易结果
    url(r'^comment/(?P<order_id>\d+)/$', OrderCommentView.as_view(),name='comment')
]
