#coding:utf-8
from . import app_user
from flask import render_template


@app_user.route('/')
def user_index():
    return render_template('user.html')