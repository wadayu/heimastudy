#coding:utf-8
from flask import Flask
from werkzeug.routing import BaseConverter

app = Flask(__name__)

# 1、定义转换器
class ReConverter(BaseConverter):
    def __init__(self,url_map,regex):
        super(ReConverter, self).__init__(url_map)
        self.regex = regex

# 2、将自定义的转换器添加到flask应用中
app.url_map.converters['re'] = ReConverter


@app.route("/good_id/<int:num>")
def index(num):
    return 'This is %s' %num


@app.route("/send/<re(r'1[345678]\d{9}'):mobile>")
def send_phone(mobile):
    return 'Send  mobile %s' %mobile


if __name__ == '__main__':
    print (app.url_map)
    app.run(debug=True)