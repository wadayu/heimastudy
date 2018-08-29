"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import xadmin

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^search/', include('haystack.urls')), # 全文检索框架
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^order/', include('order.urls', namespace='order')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^', include('goods.urls', namespace='goods')),

    # 富文本编辑器
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
]

# 全局404页面配置
handler404 = 'user.views.page_notfound'
# 全局500页面配置
handler500 = 'user.views.page_error'