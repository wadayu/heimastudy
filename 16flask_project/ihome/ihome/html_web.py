#coding:utf-8
from flask import Blueprint,current_app,make_response
from flask_wtf import csrf

html = Blueprint('html',__name__)


@html.route("/<re(r'.*'):file_name>")
def html_static(file_name):
    # if not file_name:
    #     file_name = 'index.html'
    #
    if file_name != 'favicon.ico':
        file_name = 'html/' + file_name
    # 生成csrf值
    csrf_token = csrf.generate_csrf()
    # 在cookie里设置csrf_token
    response = make_response(current_app.send_static_file(file_name))
    response.set_cookie('csrf_token',csrf_token)
    # flask返回静态文件的方法
    return response