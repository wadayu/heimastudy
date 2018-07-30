
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),

    # ajax测试
    url(r'^login/$', views.login, name='login'),
    url(r'^check_pass/$', views.check_pass, name='check_pass'), # ajax验证

    # cookie测试
    url(r'^login_cookie/$', views.login_cookie, name='login_cookie'), # login cookie保存
    url(r'^check_cookie/$', views.check_cookie, name='check_cookie'),

    # session测试
    url(r'login_session/$', views.login_session, name='login_session'),
    url(r'check_session/$', views.check_session, name='check_session'),

    # 修改密码的url
    url(r'change_pwd/$', views.change_pwd, name='change_pwd'),
    # 修改密码状态
    url(r'change_pwd_action/$', views.change_pwd_ation, name='change_pwd_ation'),
    
    #template变量
    url(r'template_vars/$', views.template_vars, name='template_vars'),

    # 验证码url
    url(r'verify_code/$', views.verify_code, name='verify_code'),

    # 图片上传
    url (r'upload_show/$', views.upload_show, name='upload_show'),
    # 图片处理
    url(r'upload_handle', views.uplaod_handle, name='uplaod_handle')
]
