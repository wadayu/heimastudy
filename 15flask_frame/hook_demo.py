#coding:utf-8
from flask import Flask,request,url_for

app = Flask(__name__)

"""flask的hook类似与django的中间件，只是flask的hook影响全局视图函数，即每个视图运行的时候都调用hook"""

@app.before_first_request
# 视图被调用之前执行的函数并且是第一次请求
def before_first_request():
    print ('before_first_request view running')

@app.before_request
# 视图被调用之前执行的函数
def before_request():
    print ('before_request view running')

@app.after_request
# 视图被调用之后执行的函数 （前提视图函数没有抛出异常）
def after_request(response):
    print ('after_request view running')
    return response

@app.teardown_request
# 视图被调用之后执行的函数 （视图函数不管有没有抛出异常，都会被执行，并且debug=false的情况下）
def teardown_request(response):
    # 如果针对某一个视图函数操作可以通过以下方法实现
    if request.path == url_for('index'):
        print url_for('index')
    elif request.path == url_for('login'):
        print url_for('login')
    return response

@app.route('/')
def index():
    print ('index view running')
    return 'index'

@app.route('/login')
def login():
    return 'login'

if __name__ == '__main__':
    print (app.url_map)
    app.run(debug=True)