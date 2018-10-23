#coding:utf-8
import redis,os


class Config(object):
    # 配置数据库的连接
    SQLALCHEMY_DATABASE_URI = 'mysql://flask:flask@192.168.19.131:3306/ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = True # 设置sqlalchemy自动更跟踪数据库

    # flask-session配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host='192.168.19.131', port=6379,db=11)
    SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏处理
    PERMANENT_SESSION_LIFETIME = 3600*24*7 # session数据的有效期，单位秒

    # redis的存储参数配置
    REDIS_HOST = '192.168.19.131'
    REDIS_PORT = 6379
    REDIS_DB = 10

    SECRET_KEY = 'n+g1z1rh9i*rhalu_2cqc+m^n7^h@b+_m-4(mlunhh9872nm)pwerq2699w32645865'

class DeveConfig(Config):
    """开发环境"""
    FDFS_CLIENT_CONF = 'ihome/utils/fdfs/client.conf'
    IMAGE_STORAGE_URL = 'http://192.168.19.131:8888/'
    DEBUG = True
    pass

class ProdConfig(Config):
    """生产环境"""
    pass

config_map = {
    'deve':DeveConfig,
    'prod':ProdConfig
}
