#coding:utf-8

from django.conf import settings
from django.core.mail import send_mail
from django.template import loader, RequestContext
from celery import Celery

import os,sys,io

# 在worker一端加这几句
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
# django.setup()

from goods.models import IndexGoodsBanner,GoodsType,IndexPromotionBanner,GoodsSKU

# worker端运行的命令（运行的环境要和项目端的环境一致）
# celery -A celery_tasks.tasks worker  -l info --logfile=/data/log/celery.log（指定日志文件路径）

# 创建一个Celery类的实例对象 pip install celery,redis
app = Celery('celery_tasks', broker='redis://192.168.19.131:6379/5')


@app.task
def send_register_email(username,email,token):
    # 异步发送邮件消息队列
    subject = '天天生鲜欢迎信息'
    message = ''
    from_email = settings.EMAIL_FROM
    receiver = [email]
    html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
        username, token, token)

    send_mail(subject, message, from_email, receiver, html_message=html_message)

@app.task
def send_update_email(email,token):
    # 异步发送邮件消息队列
    subject = '天天生鲜用户密码找回'
    message = ''
    from_email = settings.EMAIL_FROM
    receiver = [email]
    html_message = '请点击下面的链接重设你的密码<br/><a href="http://127.0.0.1:8000/user/modify_pwd/%s">http://127.0.0.1:8000/user/modify_pwd/%s</a>' % (token, token)

    send_mail(subject, message, from_email, receiver, html_message=html_message)

@app.task
def generate_static_index_html():
    """生成静态页面 在worker端生成静态页面"""
    # 所有的商品类型
    all_types = GoodsType.objects.all()
    # 所有的轮播图片
    all_banners = IndexGoodsBanner.objects.all().order_by('index')
    # 所有的活动展示图
    all_promotionbanners = IndexPromotionBanner.objects.all().order_by('index')
    # 循环商品的种类
    for type in all_types:
        # 获取每个种类的前四个商品
        all_goods = GoodsSKU.objects.filter(type=type)[:4]
        # 动态给type增加属性
        type.all_goods = all_goods

    # 获取用户购物车的列表数量
    cart_count = 0

    context = {
        'all_types': all_types,
        'all_banners': all_banners,
        'all_promotionbanners': all_promotionbanners,
    }

    # 使用模板
    # 1.加载模板文件,返回模板对象
    temp = loader.get_template('static_index.html')
    # 2.模板渲染
    static_index_html = temp.render(context)

    # 生成首页对应静态文件
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path, 'w') as f:
        f.write(static_index_html)

