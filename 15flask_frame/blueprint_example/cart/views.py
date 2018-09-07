#coding:utf-8

from flask import render_template

from . import app_cart

@app_cart.route('/info')
def cart_index():
    return render_template('cart.html')