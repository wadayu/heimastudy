#coding:utf-8
from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand

from user import app_user
from goods import app_goods
from cart import app_cart

app = Flask(__name__)

class Config(object):
    # 配置数据库的连接
    SQLALCHEMY_DATABASE_URI = 'mysql://flask:flask@192.168.19.131:3306/flask_py2'
    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SECRET_KEY = 'n+g1z1rh9i*rhalu_2cqc+m^n7^h@b+_m-4(mlunhh9872nm)p'

# 添加配置参数到app中
app.config.from_object(Config)
# 将app加入到管理模块
manager = Manager(app)
# 创建db对象
db = SQLAlchemy(app)
# 将migrate和app db做一个关联
Migrate(app, db)
# 向manager对象添加管理数据库的命令
manager.add_command('db',MigrateCommand)

# 注册蓝图（flask的蓝图类似django的app模块）  url_prefix（类似django的namespace）
app.register_blueprint(app_user,url_prefix='/user')
app.register_blueprint(app_goods,url_prefix='/goods')
app.register_blueprint(app_cart,url_prefix='/cart')

if __name__ == '__main__':
    # print (app.url_map)
    manager.run()

# 启动gunicorn 命令
# gunicorn -c gunicorn.conf main:app