#coding:utf-8
from flask import request,g,jsonify,current_app

from datetime import datetime

from . import api
from ihome.utils.response_code import RET
from ihome.models import House,Order,User
from ihome import db,redis_conn
from ihome.utils.commons import login_required

#POST /api/v1.0/place/order
@api.route('/place/order',methods=['POST'])
@login_required
def save_order():
    """创建订单"""
    user_id = g.user_id
    # 获取参数
    order_data = request.get_json() # 将json数据转化为字典
    if not order_data:
        return jsonify(errno=RET.PARAMERR, errmsg=u'未获取到数据')

    house_id = order_data.get('house_id')
    start_time = order_data.get('sd')
    end_time = order_data.get('ed')

    if not all([house_id,start_time,end_time]):
        return jsonify(errno=RET.PARAMERR,errmsg=u'参数不完整')

    # 校验日期
    try:
        start_time = datetime.strptime(start_time,'%Y-%m-%d')
        end_time = datetime.strptime(end_time, '%Y-%m-%d')
        assert start_time <= end_time
        days = (end_time - start_time).days + 1
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg=u'日期有误')

    # 判断用户是否有尚未支付的订单 如果有就不能下订单
    try:
        wait_pay_count = Order.query.filter_by(user_id=user_id,status='WAIT_PAYMENT').count()
    except Exception as e:
        current_app.logger.error(e)

    if wait_pay_count >= 1:
        return jsonify(errno=RET.SERVERERR, errmsg=u'你有未支付的订单，请先支付')

    # 校验房屋id
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'获取房屋数据失败')

    if not house:
        return jsonify(errno=RET.DATAEXIST, errmsg=u'房屋不存在')

    # 判断入住的天数不能大于最大的入住天数
    if house.max_days != 0 and days > house.max_days:
        return jsonify(errno=RET.DATAERR, errmsg=u'不能入住，此房屋最大入住天数为%s天' %house.max_days)

    if house.user_id == user_id:
        return jsonify(errno=RET.DATAERR, errmsg="自己不能预定自己的房间")

    #检查房屋是否被订单
    try:
        count = Order.query.filter(Order.house_id==house_id, Order.begin_date <= end_time,\
                                   Order.end_date >= start_time).count()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="检查出错，请稍候重试")

    if count > 0:
        return jsonify(errno=RET.DATAERR, errmsg="房间已经被预定")

    # 总价格
    amount = house.price * days

    try:
        order = Order(user_id=user_id,house_id=house_id,begin_date=start_time,\
                      end_date=end_time,days=days,house_price=house.price,amount=amount)
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="创建订单失败")

    return jsonify(errno=RET.OK, errmsg="订单创建成功")


# GET /api/v1.0/user/orders
@api.route('/user/orders',methods=['GET'])
@login_required
def get_user_orders():
    """获取用户的所有订单"""
    user_id = g.user_id

    # 查询用户的所有订单
    try:
        orders = Order.query.filter(Order.user_id == user_id).order_by(Order.create_time.desc()).all()
        # user = User.query.get(user_id)
        # orders = user.orders
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'查询数据失败')

    all_orders = []
    for order in orders:
        all_orders.append(order.to_basic_dict())

    return  jsonify(errno=RET.OK,errmsg=u'ok',data={'all_orders':all_orders})


# Get /api/v1.0/user/customer/orders
@api.route('/user/customer/orders',methods=['GET'])
@login_required
def get_customer_orders():
    """查询自己的房源被客户下过的订单"""
    user_id = g.user_id

    try:
        user = User.query.get(user_id)
        houses = user.houses  # 获取用户所有的房子
        house_ids = [house.id for house in houses] # 获取房子的id
        orders = Order.query.filter(Order.house_id.in_(house_ids)).order_by(Order.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'获取数据失败')

    all_orders = []
    for order in orders:
        all_orders.append(order.to_basic_dict())

    return  jsonify(errno=RET.OK,errmsg=u'ok',data={'all_orders':all_orders})

#PUT /api/v1.0/order/status/1
@api.route('/order/status/<int:order_id>',methods=['PUT'])
@login_required
def order_accept_reject(order_id):
    """更订单状态"""
    user_id = g.user_id
    # 接收参数
    res_data = request.get_json()
    if not res_data:
        return jsonify(errno=RET.PARAMERR,errmsg=u'参数错误')
    action = res_data.get('action','')
    if action not in ("accept", "reject"):
        return jsonify(errno=RET.PARAMERR, errmsg=u'参数错误')

    try:
        order = Order.query.filter(Order.id == order_id,Order.status == 'WAIT_ACCEPT').first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'获取订单失败')

    if not order or order.house.user_id != user_id:
        return jsonify(errno=RET.DATAERR, errmsg=u'操作无效')

    if action == 'accept':
        order.status = 'WAIT_PAYMENT'
    elif action == 'reject':
        reason = res_data.get('reason','')
        if not reason:
            return jsonify(errno=RET.PARAMERR, errmsg=u"参数错误")
        order.status = 'REJECTED'
        order.comment = reason

    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u"操作失败")

    return jsonify(errno=RET.OK, errmsg="OK")

# PUT /api/v1.0/order/comment/1
@api.route('/order/comment/<int:order_id>',methods=['PUT'])
@login_required
def order_comment(order_id):
    """订单评论提交"""
    user_id = g.user_id

    res_data = request.get_json()
    if not res_data:
        return jsonify(errno=RET.PARAMERR,errmsg=u'参数错误')

    comment = res_data.get('comment','')
    if not comment:
        return jsonify(errno=RET.DATAEXIST,errmsg=u'评价信息不能为空！')

    try:
        order = Order.query.filter(Order.id == order_id,Order.user_id == user_id,\
                                   Order.status == 'WAIT_COMMENT').first()
        house = order.house
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'获取数据失败')

    if not order:
        return jsonify(errno=RET.DATAERR, errmsg=u'操作无效数据')

    try:
        # 更改订单状态
        order.status = 'COMPLETE'
        order.comment = comment
        # 房屋的订单数+1
        house.order_count += 1
        db.session.add(order)
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg=u'操作数据失败')

    # 删除缓存数据
    try:
        cache_data = redis_conn.delete('house_detail_%s' %house.id)
    except Exception as e:
        current_app.logger.error(e)

    return  jsonify(errno=RET.OK,errmsg='ok')