#coding:utf-8
from flask import render_template
from . import app_goods

@app_goods.route('/info')
def goods_index():
    return render_template('goods.html')