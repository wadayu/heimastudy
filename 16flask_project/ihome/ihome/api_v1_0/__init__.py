#coding:utf-8
from flask import Blueprint

# 创建蓝图
api = Blueprint('api_v1_0',__name__)

from .views import *
from .houses import *