from django.conf.urls import url

from user.views import RegisterView,ActiveView,LoginView,LogoutView,UpdatePwdView,ModifyPwdView,ResetPwdView
from user.views import UserInfoView,UserOrderView,UserAddressView,UpdateDefaultAddressView,UserCommentView

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(),name='register'), # 注册
    url(r'^active/(?P<token>.*)/$', ActiveView.as_view(),name='active'), # 用户激活
    url(r'^login/$', LoginView.as_view(),name='login'), # 登录
    url(r'^update_pwd/$', UpdatePwdView.as_view(),name='update_pwd'), # 找回密码页面
    url(r'^modify_pwd/(?P<token>.*)/$', ModifyPwdView.as_view(),name='modify_pwd'), #修改密码
    url(r'^reset_pwd/$', ResetPwdView.as_view(),name='reset_pwd'), #重设密码
    url(r'^logout/$', LogoutView.as_view(),name='logout'), # 退出

    url(r'^info/$', UserInfoView.as_view(),name='user_info'), #个人中心
    url(r'^order/$', UserOrderView.as_view(),name='user_order'), #个人订单
    url(r'^address/$', UserAddressView.as_view(),name='user_address'), #个人收货地址
    url(r'^update_address', UpdateDefaultAddressView.as_view(), name='update_address'), # 更改默认收货地址
    url(r'^comment/$',UserCommentView.as_view(),name='comment') #用户评论
]
