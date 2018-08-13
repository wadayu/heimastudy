from django.conf.urls import url

from user.views import RegisterView,ActiveView,LoginView,LogoutView
from user.views import UserInfoView,UserOrderView,UserAddressView,UpdateDefaultAddressView

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(),name='register'), # 注册
    url(r'^active/(?P<token>.*)/$', ActiveView.as_view(),name='active'), # 用户激活
    url(r'^login/$', LoginView.as_view(),name='login'), # 登录
    url(r'^logout/$', LogoutView.as_view(),name='logout'), # 退出

    url(r'^info/$', UserInfoView.as_view(),name='user_info'), #个人中心
    url(r'^order/$', UserOrderView.as_view(),name='user_order'), #个人订单
    url(r'^address/$', UserAddressView.as_view(),name='user_address'), #个人收货地址
    url(r'^update_address', UpdateDefaultAddressView.as_view(), name='update_address') # 更改默认收货地址
]
