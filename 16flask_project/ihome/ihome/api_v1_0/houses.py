# coding:utf8
from flask import jsonify,current_app,g,request,session

import json,datetime

from . import api
from ihome.models import Area,House,Facility,HouseImage,User,Order
from ihome.utils.response_code import RET
from ihome.utils.fdfs.storage import FDFSStorage
from ihome import redis_conn,db
from ihome.utils.commons import login_required

# GET /api/v1.0/areas
@api.route('/areas')
def get_areas():
    """
    获取地区地址
    :return: 返回地址信息
    """
    # 尝试从缓存里获取数据，如果没有从读数据库获取
    try:
        areas_dict = redis_conn.get('areas_info') # string
    except Exception as e:
        current_app.logger.error(e)


    if areas_dict:
        areas_dict = eval(areas_dict) # string --> dict
    else:
        try:
            all_areas = Area.query.all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DATAERR,errmsg=u'数据库错误')

        areas_dict = {}
        for area in all_areas:
            areas_dict[area.id] = area.name
        # 将数据缓存到redis
        try:
            redis_conn.setex('areas_info',3600,areas_dict)
        except Exception as e:
            current_app.logger.error(e)

    return jsonify(errno=RET.OK,data=areas_dict)

# POST /api/v1.0/houses/info
@api.route("/houses/info", methods=["POST"])
@login_required
def save_house_info():
    """保存房屋的基本信息
    前端发送过来的json数据
    {
        "title":"",
        "price":"",
        "area_id":"1",
        "address":"",
        "room_count":"",
        "acreage":"",
        "unit":"",
        "capacity":"",
        "beds":"",
        "deposit":"",
        "min_days":"",
        "max_days":"",
        "facility":["7","8"]
    }
    """
    # 获取数据
    user_id = g.user_id
    house_data = request.get_json()

    # 验证用户是否实名
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)

    if not (user.real_name and user.id_card):
        return jsonify(errno=RET.DATAEXIST,errmsg=u'用户未实名认证，不能发布房源')

    title = house_data.get("title")  # 房屋名称标题
    price = house_data.get("price")  # 房屋单价
    area_id = house_data.get("area_id")  # 房屋所属城区的编号
    address = house_data.get("address")  # 房屋地址
    room_count = house_data.get("room_count")  # 房屋包含的房间数目
    acreage = house_data.get("acreage")  # 房屋面积
    unit = house_data.get("unit")  # 房屋布局（几室几厅)
    capacity = house_data.get("capacity")  # 房屋容纳人数
    beds = house_data.get("beds")  # 房屋卧床数目
    deposit = house_data.get("deposit")  # 押金
    min_days = house_data.get("min_days")  # 最小入住天数
    max_days = house_data.get("max_days")  # 最大入住天数

    # 校验参数
    if not all([title, price, area_id, address, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 判断金额是否正确
    try:
        price = int(float(price) * 100)
        deposit = int(float(deposit) * 100)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 判断城区id是否存在
    try:
        area = Area.query.get(area_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    if area is None:
        return jsonify(errno=RET.NODATA, errmsg="城区信息有误")

    # 保存房屋信息
    house = House(
        user_id=user_id,
        area_id=area_id,
        title=title,
        price=price,
        address=address,
        room_count=room_count,
        acreage=acreage,
        unit=unit,
        capacity=capacity,
        beds=beds,
        deposit=deposit,
        min_days=min_days,
        max_days=max_days
    )

    # 处理房屋的设施信息
    facility_ids = house_data.get("facility")

    # 如果用户勾选了设施信息，再保存数据库
    if facility_ids:
        # ["7","8"]
        try:
            # select  * from ih_facility_info where id in []
            facilities = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="数据库异常")

        if facilities:
            # 表示有合法的设施数据
            # 保存设施数据
            house.facilities = facilities

    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存数据失败")

    # 保存数据成功
    return jsonify(errno=RET.OK, errmsg="OK", data={"house_id": house.id})


# POST /api/v1.0/houses/images
@api.route('/houses/images',methods=['POST'])
@login_required
def save_house_image():
    """
    保存房屋的图片
    :return: 房屋图片的url
    """
    image_data = request.files.get('house_image')
    house_id = request.form.get('house_id')

    if not all([image_data,house_id]):
        return jsonify(errno=RET.DATAERR, errmsg="参数不完整")

    # 判断房屋id是否存在
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)

    if not house:
        return jsonify(errno=RET.DBERR, errmsg="房屋id不存在")

    # 将客户上传的图片存储到fastdfs
    storage = FDFSStorage(client_conf=current_app.config.get('FDFS_CLIENT_CONF'))
    try:
        file_url = storage.save_file(image_data.filename, image_data)
    except Exception as e:
        return jsonify(errno=RET.DATAERR, errmsg=u'上传图片失败')

    # 保存图片url到数据库
    house_image = HouseImage(house_id=house_id,url=file_url)
    db.session.add(house_image)

    if not house.index_image_url:
        house.index_image_url = file_url
        db.session.add(house)

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DATAERR, errmsg=u'图片保存失败')
    # 图片完整的url
    image_url = current_app.config.get('IMAGE_STORAGE_URL') + file_url
    return jsonify(errno=RET.OK,errmsg='ok',data={'image_url':image_url})


# GET /api/v1.0/user/houses
@api.route('/user/houses')
@login_required
def get_user_house():
    """
    获取用户发布的房源信息
    :return: 用户房源的基本信息
    """
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
        houses = user.houses
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'获取用户信息失败')

    houses_list = []
    for house in houses:
        houses_list.append(house.to_basic_dict())
    return '{"errno":0,"errmsg":"ok","data":%s}' %json.dumps(houses_list),200,{"Content-Type": "application/json"}


# GET /api/v1.0/house/detail/<house_id>
@api.route('/house/detail/<int:house_id>')
def get_house_detail(house_id):
    """
    展示房屋的详细信息
    前端在房屋详情页面展示时，如果浏览页面的用户不是该房屋的房东，则展示预定按钮，否则不展示，
    所以需要后端返回登录用户的user_id
    尝试获取用户登录的信息，若登录，则返回给前端登录用户的user_id，否则返回user_id=-1
    :param house_id: int<house_id>
    :return: json
    """
    user_id = session.get('user_id',0)

    # 检查参数
    if not house_id:
        return jsonify(errno=RET.PARAMERR,errmsg=u'参数错误')

    # 尝试从redis读取缓存
    try:
        cache_data = redis_conn.get('house_detail_%s' %house_id)
    except Exception as e:
        current_app.logger.error(e)
    if cache_data:
        print ('从redis中读取缓存数据')
        response = {'errno': RET.OK, 'errmsg': u'ok', 'data': {'user_id': user_id, 'house_info': eval(cache_data)}}
        return json.dumps(response), 200, {'Content-Type': 'application/json'}

    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'查询失败')

    if not house:
        return jsonify(errno=RET.DATAEXIST, errmsg=u'房屋不存在')
    # 获取详细信息（dict）
    house_data = house.to_full_dict()
    # json_data = json.dumps(house_data)

    # 设置缓存数据
    try:
        redis_conn.setex('house_detail_%s' %house_id,3600,house_data)
    except Exception as e:
        current_app.logger.error(e)

    response = {'errno':RET.OK,'errmsg':u'ok','data':{'user_id':user_id,'house_info':house_data}}

    return json.dumps(response),200,{'Content-Type':'application/json'}

# GET /api/v1.0/houses/index
@api.route('/houses/index',methods=['GET'])
def get_houses_index():
    """
    获取房屋的index_image_url图片，并展示到主页
    :return: image_urls
    """
    # 尝试从redis获取缓存
    try:
        cache_data = redis_conn.get('index_urls_data')
    except Exception as e:
        current_app.logger.error(e)

    if cache_data:
        print ('从redis读取数据')
        response = {'errno': RET.OK, 'errmsg': 'ok', 'data': {'houses_info': eval(cache_data)}}
        return json.dumps(response), 200, {'Content-Type': 'application/json'}

    try:
        houses = House.query.order_by(House.order_count.desc()).limit(5)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'获取数据失败')

    index_data = []

    for house in houses:
        if not house.index_image_url:
            continue
        index_data.append({'img_url':current_app.config.get('IMAGE_STORAGE_URL') + house.index_image_url,
                           'title':house.title,
                           'house_id':house.id})

    # 设置缓存
    try:
        redis_conn.setex('index_urls_data',3600,index_data)
    except Exception as e:
        current_app.logger.error(e)

    response = {'errno':RET.OK,'errmsg':'ok','data':{'houses_info':index_data}}
    return json.dumps(response),200,{'Content-Type':'application/json'}


# GET /api/v1.0/houses?sd=2017-12-01&ed=2017-12-31&aid=10&sk=new&p=1
@api.route("/houses")
def get_house_list():
    """获取房屋的列表信息（搜索页面）"""
    start_date = request.args.get("sd", "")  # 用户想要的起始时间
    end_date = request.args.get("ed", "")  # 用户想要的结束时间
    area_id = request.args.get("aid", "")  # 区域编号
    sort_key = request.args.get("sk", "new")  # 排序关键字
    page = request.args.get("p")  # 页数

    # 处理时间
    try:
        if start_date:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")

        if end_date:
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        if start_date and end_date:
            assert start_date <= end_date
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="日期参数有误")

    # 判断区域id
    if area_id:
        try:
            area = Area.query.get(area_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg="区域参数有误")

    # 处理页数
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    # 获取缓存数据
    redis_key = "house_%s_%s_%s_%s" % (start_date, end_date, area_id, sort_key)
    try:
        resp_json = redis_conn.hget(redis_key, page)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json:
            return resp_json, 200, {"Content-Type": "application/json"}

    # 过滤条件的参数列表容器
    filter_params = []

    # 填充过滤参数
    # 时间条件
    conflict_orders = None

    try:
        if start_date and end_date:
            # 查询冲突的订单
            conflict_orders = Order.query.filter(Order.begin_date <= end_date, Order.end_date >= start_date).all()
        elif start_date:
            conflict_orders = Order.query.filter(Order.end_date >= start_date).all()
        elif end_date:
            conflict_orders = Order.query.filter(Order.begin_date <= end_date).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    if conflict_orders:
        # 从订单中获取冲突的房屋id
        conflict_house_ids = [order.house_id for order in conflict_orders]

        # 如果冲突的房屋id不为空，向查询参数中添加条件
        if conflict_house_ids:
            filter_params.append(House.id.notin_(conflict_house_ids))

    # 区域条件
    if area_id:
        filter_params.append(House.area_id == area_id)

    # 查询数据库
    # 补充排序条件
    if sort_key == "booking":  # 入住做多
        house_query = House.query.filter(*filter_params).order_by(House.order_count.desc())
    elif sort_key == "price-inc":
        house_query = House.query.filter(*filter_params).order_by(House.price.asc())
    elif sort_key == "price-des":
        house_query = House.query.filter(*filter_params).order_by(House.price.desc())
    else:  # 新旧
        house_query = House.query.filter(*filter_params).order_by(House.create_time.desc())

    # 处理分页
    try:
        #                               当前页数          每页数据量                              自动的错误输出
        page_obj = house_query.paginate(page=page, per_page=2, error_out=False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    # 获取页面数据
    house_li = page_obj.items
    houses = []
    for house in house_li:
        houses.append(house.to_basic_dict())

    # 获取总页数
    total_page = page_obj.pages

    resp_dict = dict(errno=RET.OK, errmsg="OK", data={"total_page": total_page, "houses": houses, "current_page": page})
    resp_json = json.dumps(resp_dict)

    if page <= total_page:
        # 设置缓存数据
        redis_key = "house_%s_%s_%s_%s" % (start_date, end_date, area_id, sort_key)
        # 哈希类型
        try:
            # redis_conn.hset(redis_key, page, resp_json)
            # redis_conn.expire(redis_key, constants.HOUES_LIST_PAGE_REDIS_CACHE_EXPIRES)

            # 创建redis管道对象，可以一次执行多个语句
            pipeline = redis_conn.pipeline()

            # 开启多个语句的记录
            pipeline.multi()

            pipeline.hset(redis_key, page, resp_json)
            pipeline.expire(redis_key, 3600)

            # 执行语句
            pipeline.execute()
        except Exception as e:
            current_app.logger.error(e)

    return resp_json, 200, {"Content-Type": "application/json"}


# redis_conn
#
# "house_起始_结束_区域id_排序_页数"
# (errno=RET.OK, errmsg="OK", data={"total_page": total_page, "houses": houses, "current_page": page})
#
#
#
# "house_起始_结束_区域id_排序": hash
# {
#     "1": "{}",
#     "2": "{}",
# }
