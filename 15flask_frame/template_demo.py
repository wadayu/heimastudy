#coding:utf-8
from flask import Flask,render_template

app = Flask(__name__)



@app.template_filter('filter')
# 自定义过滤器
def custom_filter(args):
    return  args[::2]

# 自定义过滤器另外一种方法
def custom_filter2(args):
    return args[1::2]

app.add_template_filter(custom_filter2,'filter2')


@app.route('/')
def index():
    context = {'username':'python',
               'gender':'female',
               'my_list':[1,2,3,4,5,6,7],
               'content':'<b>Hello World</b>'
               }
    return render_template('index.html',**context)


if __name__ == '__main__':
    app.run(debug=True)