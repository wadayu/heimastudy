#coding:utf-8

from django.conf import settings
from django.core.mail import send_mail

from celery import Celery

# 在worker一端加这几句
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
# django.setup()

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