#coding:utf-8
from flask import g,current_app,request,jsonify,make_response
from alipay import AliPay

import os

from ihome import db
from ihome.api_v1_0 import api
from ihome.utils.commons import login_required
from ihome.models import Order
from ihome.utils.response_code import RET

#POST /api/v1.0/order/pay
@api.route('/order/pay',methods=['POST'])
@login_required
def order_pay():
    """订单支付页面（给用户返回支付宝的支付链接）"""
    user_id = g.user_id
    # 获取订单id
    order_id = request.get_json().get('order_id','')
    if not order_id:
        return jsonify(errno=RET.DATAERR, errmsg=u'无效订单id')

    try:
        order = Order.query.filter_by(id=order_id,user_id=user_id,status='WAIT_PAYMENT').first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'查询数据异常')

    if not order:
        return jsonify(errno=RET.DATAERR, errmsg=u'订单异常')

    # 构造支付宝链接

    alipay = AliPay(
        appid="2016091800536571",  # 应用id
        app_notify_url="http://ihome.ygege.com.cn/api/v1.0/order/pay/result",  # 默认回调url
        app_private_key_path=os.path.join(os.path.dirname(__file__), 'keys/app_private_key.pem'),
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), 'keys/alipay_public_key.pem'),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    # 调用支付接口
    # 手机网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_wap_pay(
        out_trade_no=order.id,  # 订单id
        total_amount=str(order.amount/100),  # 支付总金额
        subject=u'爱家订单支付-%s'.encode('utf8')  %order_id,
        return_url=None,
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    # 返回应答
    pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
    return jsonify(errno=RET.OK, data={'pay_url':pay_url})


#POST /api/v1.0/order/pay/result
@api.route('/order/pay/result',methods=['POST'])
def order_pay_result():
    """用户订单的返回结果"""
    data = request.form.to_dict()
    """
    data = {
        "subject": "测试订单",
        "gmt_payment": "2016-11-16 11:42:19",
        "charset": "utf-8",
        "seller_id": "xxxx",
        "trade_status": "TRADE_SUCCESS",
        "buyer_id": "xxxx",
        "auth_app_id": "xxxx",
        "buyer_pay_amount": "0.01",
        "version": "1.0",
        "gmt_create": "2016-11-16 11:42:18",
        "trade_no": "xxxx",
        "fund_bill_list": "[{\"amount\":\"0.01\",\"fundChannel\":\"ALIPAYACCOUNT\"}]",
        "app_id": "xxxx",
        "notify_time": "2016-11-16 11:42:19",
        "point_amount": "0.00",
        "total_amount": "0.01",
        "notify_type": "trade_status_sync",
        "out_trade_no": "xxxx",
        "buyer_logon_id": "xxxx",
        "notify_id": "xxxx",
        "seller_email": "xxxx",
        "receipt_amount": "0.01",
        "invoice_amount": "0.01",
        "sign": "xxx"
    }
    """
    # sign 不能参与签名验证
    signature = data.pop("sign")

    alipay = AliPay(
        appid="2016091800536571",  # 应用id
        app_notify_url="http://ihome.ygege.com.cn/api/v1.0/order/pay/result",  # 默认回调url
        app_private_key_path=os.path.join(os.path.dirname(__file__), 'keys/app_private_key.pem'),
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), 'keys/alipay_public_key.pem'),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    # verify
    pay_status = alipay.verify(data, signature)

    order_id = data.get('out_trade_no','')
    trade_no = data.get('trade_no','')
    order_id = order_id.encode('utf8')
    trade_no = trade_no.encode('utf8')

    if pay_status and data["trade_status"] == "TRADE_SUCCESS":
        try:
            Order.query.filter_by(id=order_id).update({'status':'WAIT_COMMENT','trade_no':trade_no})
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)

        current_app.logger.info('订单（订单号：%s）支付成功' %order_id)
        response = make_response('success')
        return response, 200
    else:
       current_app.logger.error('订单（订单号：%s）支付失败' %order_id)
       response = make_response('failed')
       return response, 400
