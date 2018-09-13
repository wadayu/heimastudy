#coding:utf-8
from flask import Blueprint

app_goods = Blueprint('app_goods',__name__)

from .views import *