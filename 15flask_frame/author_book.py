#coding:utf-8
from flask import Flask,render_template,redirect,url_for,request,jsonify
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField
from wtforms.validators import DataRequired

from datetime import datetime
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

class Config(object):
    # 配置数据库的连接
    SQLALCHEMY_DATABASE_URI = 'mysql://flask:flask@192.168.19.131:3306/flask_py2'
    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SECRET_KEY = 'n+g1z1rh9i*rhalu_2cqc+m^n7^h@b+_m-4(mlunhh9872nm)p'

# 将配置参数应用的app中
app.config.from_object(Config)

# 创建sqlalchemy对象
db = SQLAlchemy(app)

# 将APP加入到管理模块
manager = Manager(app)

# 将migrate 和 app db做一个对应关系
Migrate(app,db)

# 向manager管理模块添加db的命令，用于管理数据库
manager.add_command('db',MigrateCommand)

# python file db init 初始化migrate目录
# python file db migrate -m 'describ' (类似django的makemigrations)
# python file db upgrade 往数据库里创建表
# python file db history 查看migrate历史记录
# python file db downgrade 'migrate id' 历史回退

# 创建表单
class BookForm(FlaskForm):
    book_name = StringField(label=u'书籍名称',validators=[DataRequired(u'数据名称不能空')])
    author = StringField(label=u'书籍作者',validators=[DataRequired(u'作者不能空')])
    submit = SubmitField(label=u'提交')

# 创建数据表
class Author(db.Model):
    # 指定表名
    __tablename__ = 'tbl_author'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    books = db.relationship('Book',backref='author')


class Book(db.Model):
    # 指定表名
    __tablename__ = 'tbl_book'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('tbl_author.id'))


@app.route('/', methods=['GET','POST'])
def index():
    form = BookForm()
    if form.validate_on_submit():
        # form获取用户提交的数据
        book_name = form.book_name.data
        author = form.author.data

        # 数据库表创建作者
        author = Author(name=author)
        db.session.add(author)
        db.session.commit()

        # 数据库创建书籍
        book = Book(name=book_name,author_id=author.id)
        db.session.add(book)
        db.session.commit()


        return redirect(url_for('index'))
    all_books = Book.query.all()
    return render_template('books.html',books=all_books,form=form)

@app.route('/delete_book',methods=['POST'])
def delete_book():
    # get_json接收json的数据，并转换成字典
    book_id = request.form.get('book_id')

    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()

    # jsonify是把字典转换成json格式，同时设置响应头部信息类型格式 Content-Type:application/json
    return jsonify(res=0,message='successful')

if __name__ == '__main__':
    # db.create_all()
    # au_xi = Author(name='我吃西红柿')
    # au_qian = Author(name='萧潜')
    # au_san = Author(name='唐家三少')
    # db.session.add_all([au_xi, au_qian, au_san])
    # db.session.commit()
    #
    # bk_xi = Book(name='吞噬星空', author_id=au_xi.id)
    # bk_xi2 = Book(name='寸芒', author_id=au_qian.id)
    # bk_qian = Book(name='飘渺之旅', author_id=au_qian.id)
    # bk_san = Book(name='冰火魔厨', author_id=au_san.id)
    # db.session.add_all([bk_xi, bk_xi2, bk_qian, bk_san])
    # db.session.commit()
    manager.run()