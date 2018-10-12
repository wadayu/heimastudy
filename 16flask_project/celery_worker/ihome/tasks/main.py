#coding:utf-8
from celery import Celery

# 定义celery对象
app = Celery('celery_tasks')
# 引入配置信息
app.config_from_object('ihome.tasks.config')
# 自动搜索tasks任务(项目目录tasks.py的文件)
app.autodiscover_tasks(['ihome.tasks.sms'])