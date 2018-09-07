# coding:utf-8

from flask import Flask,jsonify
import json

app = Flask(__name__)

@app.route('/index')
def index():
    data = {'name':'John','age':24}
    # json_str = json.dumps(data)
    # 设置头部响应信息（Response Headers） 并返回json类型数据
    # return json_str,200,[('Content-Type','application/json')]

    # jsonify是把字典转换成json格式，同时设置响应头部信息类型格式 Content-Type:application/json
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
