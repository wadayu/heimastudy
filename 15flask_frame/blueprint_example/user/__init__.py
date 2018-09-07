#coding:utf-8
from flask import Blueprint

app_user = Blueprint('app_user',__name__)

from .views import user_index