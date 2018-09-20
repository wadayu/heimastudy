#coding:utf-8
from werkzeug.routing import BaseConverter
from flask import session,g,jsonify

import functools

from ihome.utils.response_code import RET

class RegexConverter(BaseConverter):
    """自定义转换器"""
    def __init__(self,url_map,*args):
        super(RegexConverter,self).__init__(url_map)
        regex = args[0]

# 登录函数装饰器
def login_required(func):
    @functools.wraps(func) #保持原函数的__name__ , __doc__属性值 如果不加的话则会显示wrapper的属性值
    def wrapper(*args,**kwargs):
        # 判断用户是否登录
        user_id = session.get('user_id')

        if user_id:
            # 将user_id保存到g对象中，在同一次请求的视图函数中可以通过g对象获取保存数据
            g.user_id = user_id
            return func(*args,**kwargs)
        else:
            return jsonify(errno=RET.SESSIONERR,errmsg=u'用户未登录')
    return wrapper

