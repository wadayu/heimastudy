#coding:utf-8
from flask import Flask,url_for,redirect

app = Flask(__name__)


@app.route('/')
def index():
    return 'index'

@app.route('/register')
def register():
    # url_for通过视图函数的名字 找到函数对应的url
    url = url_for('index')
    return redirect(url)

@app.route('/hello')
@app.route('/hello1')
def hello():
    return 'Hello World'

@app.route('/say',methods=['GET','POST'])
def say():
    return 'say hello'

@app.route('/method',methods=['GET']) # 默认方式get 可不写
def get():
    return 'The method is get'

@app.route('/method',methods=['POST'])
def post():
    return 'The method is post'


if __name__ == '__main__':
    # 查看flask项目中的所有路由信息
    print (app.url_map)
    app.run(debug=True)