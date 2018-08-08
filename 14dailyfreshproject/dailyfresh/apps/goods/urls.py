from django.conf.urls import url

from goods.views import IndexView

urlpatterns = [
    # 首页
    url(r'^$', IndexView.as_view(), name='index' )
]
