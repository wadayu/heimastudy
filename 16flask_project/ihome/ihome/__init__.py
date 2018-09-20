#coding:utf-8
import redis,logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_session import Session

from config import config_map
from utils.commons import RegexConverter


# # 配置日志信息
# # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
# file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
# formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# # 为刚创建的日志记录器设置日志记录格式
# file_log_handler.setFormatter(formatter)
# # 为全局的日志工具对象（flask app使用的）添加日记录器
# logging.getLogger().addHandler(file_log_handler)
# # 设置日志的记录等级
# logging.basicConfig(level=logging.D     EBUG)  # 调试debug级

# 创建数据库对象
db = SQLAlchemy()
# 创建redis连接 用来存储缓存数据
redis_conn = None

# flask工厂模式 根据不同的开发环境调用不同的配置文件
def create_app(type):
    """
    创建flask对象
    :param type: str   type = (deve,prod)
    :return: app object
    """
    app = Flask(__name__)
    # flask对象配置参数
    conf = config_map.get(type)
    app.config.from_object(conf)
    # app对象初始化db
    db.init_app(app)
    # 为flask补充csrf防护
    CSRFProtect(app)
    # 将session数据保存到redis
    Session(app)
    # redis存储配置
    global  redis_conn
    redis_conn = redis.StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'],db=app.config['REDIS_DB'])
    
    # 为flask添加转换器
    app.url_map.converters['re'] = RegexConverter
    # 注册蓝图
    from ihome.api_v1_0 import api
    app.register_blueprint(api,url_prefix='/api/v1.0')

    from ihome.html_web import html
    app.register_blueprint(html)

    return app