# coding:utf-8

from flask import Flask,request,make_response,session

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aw2SFAasldjfalowerlnxWETSDT48729sfasf'

@app.route('/set_cookie')
def set_cookie():
    """设置cookie"""
    response = make_response('set cookie success')
    response.set_cookie('username','python',max_age=3600)
    return response

@app.route('/get_cookie')
def get_cookie():
    """获取cookie"""
    res = request.cookies.get('username')
    return res

@app.route('/set_session')
def set_session():
    """设置session"""
    session['name'] = 'Tom'
    session['islogin'] = True
    return 'set session'

@app.route('/get_session')
def get_session():
    """获取session值 默认保存在cookie中"""
    name = session.get('name')
    return name

if __name__ == '__main__':
    app.run(debug=True)
