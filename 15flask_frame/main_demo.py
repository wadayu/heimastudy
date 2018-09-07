# coding:utf8
from flask import Flask,current_app

app = Flask(__name__, static_url_path='',  # 静态文件url  默认/static
                      static_folder='',    # 静态文件目录 默认static
                      template_folder='',)   # 模板文件目录 默认templates)


class Config(object):
    DEBUG = True
    # 自定义参数 必须大写
    LANGUAGE = 'python'
    FAVORATE = 'java'

# 设置参数的方式
# 1 从配置文件读取
#app.config.from_pyfile('config.cfg')

# 2 从py文件的类读取
app.config.from_object(Config)

# 3 参数少的话直接赋值
#app.config['DEBUG'] = True


@app.route('/')
def index():
    # 1 配置参数的获取
    r1 = app.config.get('LANGUAGE')
    print (r1)  # python
    # 2 和app.config不在同一文件的获取方法
    r2 = current_app.config.get('FAVORATE')
    print (r2) # java
    return 'Hello World'

if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0', port=5000)

