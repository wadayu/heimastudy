# coding:utf-8

from flask import Flask,request,abort

app = Flask(__name__)

@app.route('/login')
def login():
    username = ''
    pwd = ''
    if username != 'zhansan' or pwd != 'zhangsan':
        # 使用abort函数可以立即终止视图函数的执行，并可以返回指定的状态码 404 403 500 400
        abort(403)
    return 'login successfull'

@app.route('/')
def index():
    abort(500)
    return 'Welcome to BeiJing'

# 自定义404错误信息
@app.errorhandler(404)
def handler_404_error(err):
    return  'Sorry,页面没找到！当前的错误信息：%s' %err

# 自定义500错误信息
@app.errorhandler(500)
def handler_500_error(err):
    return  'Sorry,服务器内部错误请重试！当前的错误信息：%s' %err


if __name__ == '__main__':
    app.run(debug=True)
