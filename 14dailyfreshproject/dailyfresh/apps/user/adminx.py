#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/8/7 15:49'

import xadmin
from xadmin import views

from user.models import User
from user.models import Address

# 设置显示主题
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

# 设置title和footer
class GlobalSetting(object):
    site_title = '天天生鲜后台管理系统'
    site_footer = 'CopyRight © 2018 北京天天生鲜信息技术有限公司 All Rights Reserved'
    menu_style = 'accordion' # 设置折叠菜单


class AddressAdmin(object):
    list_display = ['user', 'receiver', 'addr', 'zip_code','phone','is_default','create_time','update_time','is_delete']
    search_fields = ['user', 'receiver', 'addr', 'zip_code','phone','is_default','create_time','update_time','is_delete']
    list_filter = ['user__username', 'receiver', 'addr', 'zip_code','phone','is_default','create_time','update_time','is_delete']
    model_icon = 'fa fa-truck'

xadmin.site.register(Address,AddressAdmin)

# 后台配置注册
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)

