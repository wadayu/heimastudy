#coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import pymysql
# python2中如果使用pymysql的话，必须执行pymysql.install_as_MySQLdb()
pymysql.install_as_MySQLdb()

app = Flask(__name__)

class Config(object):
    # 配置数据库的连接
    SQLALCHEMY_DATABASE_URI = 'mysql://flask:flask@192.168.19.131:3306/flask_py2'
    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

# 将配置参数添加到app对象
app.config.from_object(Config)

# 创建sqlalchemy对象
db = SQLAlchemy(app)

class Roles(db.Model):
    # 定义表名
    __tablename__ = 'tbl_roles'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128),nullable=False,unique=True)
    users = db.relationship('User',backref='role')

    def __repr__(self):
        return 'Roles Object:%s' % self.name

class User(db.Model):
    __tablename__ = 'tbl_user'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False,unique=True)
    email = db.Column(db.String(128),unique=True)
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('tbl_roles.id'))

    def __repr__(self):
        return  'User Object:%s' % self.name

if __name__ == '__main__':
    # 清除数据库中的所有表（慎用）
    db.drop_all()
    # 创建表
    db.create_all()

    # 表中添加数据
    role = Roles(name='admin')
    db.session.add(role)
    db.session.commit()

    role1 = Roles(name='staff')
    db.session.add(role1)
    db.session.commit()

    user1 = User(name='wang', email='wang@163.com', password='123456', role_id=role.id)
    user2 = User(name='zhang', email='zhang@189.com', password='201512', role_id=role1.id)
    user3 = User(name='chen', email='chen@126.com', password='987654', role_id=role.id)
    user4 = User(name='zhou', email='zhou@163.com', password='456789', role_id=role1.id)
    # 同时添加多条记录
    db.session.add_all([user1,user2,user3,user4])
    db.session.commit()




