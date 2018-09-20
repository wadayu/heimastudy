#coding:utf-8
from flask import jsonify,make_response,current_app,request,session,g
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

import random,re,json

from ihome import  redis_conn
from . import api
from ihome import db
from ihome import models
from ihome.utils.captcha.captcha import captcha
from ihome.utils.response_code import RET
from ihome.models import User
from ihome.libs.sms.sms import CCP
from ihome.utils.commons import login_required
from ihome.utils.fdfs.storage import FDFSStorage




# GET 127.0.0.1:5000/api/v1.0/image_code/<image_code_id>
@api.route('/image_codes/<image_code_id>')
def get_image_code(image_code_id):
    """
    生成验证码view
    :param image_code_id: uuid
    :return: 验证码图片
    """
    # 1、生成验证码
    name,text,image_data = captcha.generate_captcha()  # name:验证码名称 text：验证码内容 image_data:验证码图片
    # 2、将验证码保存redis
    try:
        redis_conn.setex('image_code_%s' %image_code_id,180,text ) # redis string
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg=u'保存验证码出错')
    # 3、返回验证码图片
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp

# GET 127.0.0.1:5000/api/v1.0/send_sms/<mobile>?image_code=xxxx?image_code_id=xxxx
@api.route("/sms_codes/<re(r'1[3456789]\d{9}'):mobile>")
def get_sms_code(mobile):
    """
    获取手机验证码
    :param mobile: 手机号
    :return: 发送成功状态码：0
    """
    # 获取参数
    image_code = request.args.get('image_code')
    image_code_id = request.args.get('image_code_id')
    # 校验参数
    if not all([image_code,image_code_id]):
        return jsonify(errno=RET.NODATA,errmsg=u'数据不完整')
    # 连接redis获取验证码和用户输入的对比
    try:
        real_image_code = redis_conn.get('image_code_%s' %image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'redis连接失败')

    if real_image_code is None:
        return jsonify(errno=RET.NODATA, errmsg=u'验证码已过期')

    # 删除验证码，防止一个验证码多次利用
    try:
        redis_conn.delete('image_code_%s' % image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    if real_image_code.lower() != image_code.lower():
        return jsonify(errno=RET.DATAERR, errmsg=u'验证码错误')

    # 检测用户是否在120s内连续发送短信验证码
    try:
        send_flag = redis_conn.get("send_sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if send_flag:
            return jsonify(errno=RET.REQERR, errmsg=u'请求次数过多，请120秒之后在试')

    # 校验手机号是否已经注册
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user:
            return jsonify(errno=RET.DATAEXIST, errmsg=u'用户已存在')
    #存储手机验证码到redis
    sms_code = '%06d' %random.randint(0,999999) # 随机短信验证码
    try:
        redis_conn.setex('sms_code_%s' %mobile,300,sms_code)
        # 保存发送给这个手机号的记录，防止用户在120s内再次出发发送短信的操作
        redis_conn.setex("send_sms_code_%s" % mobile, 120, 'flag')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'redis连接失败')
    # 发送短信验证码
    try:
        ccp = CCP()
        res = ccp.sendTemplateSMS(mobile,[sms_code,5],1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg=u'验证码发送异常')
    # 返回状态码
    if res == 0:
        return jsonify(errno=RET.OK, errmsg=u'验证码发送成功')
    else:
        return jsonify(errno=RET.THIRDERR, errmsg=u'验证码发送失败')


# POST 127.0.0.1:5000/api/v1.0/user/register
@api.route('/user/register',methods=['POST'])
def register():
    """
    注册view
    :return: 0：创建成功，非0：创建失败
    """
    # 获取参数
    data = request.get_json() # 获取json数据并转换成dict类型

    mobile = data.get('mobile','')
    sms_code = data.get('sms_code','')
    password = data.get('password','')
    password2 = data.get('password2','')
    # 校验参数
    if not all([mobile,sms_code,password,password2]):
        return jsonify(errno=RET.PARAMERR,errmsg=u'参数不完整')
    # 校验手机号是否合法
    res = re.match(r"1[3456789]\d{9}",mobile)
    if not res:
        return jsonify(errno=RET.PARAMERR, errmsg=u'手机号不合法')

    # 校验两次密码是否一致
    if password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg=u'两次密码不一致')

    # 判断验证码是否过期
    try:
        real_sms_code = redis_conn.get("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'redis连接失败')

    if not real_sms_code:
        return jsonify(errno=RET.PARAMERR, errmsg=u'手机验证码过期')

    # 删除手机验证码防止多次利用
    try:
        redis_conn.delete("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)

    # 校验手机验证码
    if real_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg=u'手机验证码错误')

    # 判断手机号是否注册，没有注册则创建用户
    user = User(name=mobile,mobile=mobile)
    user.password = password # 密码以密文方式存储
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e: #IntegrityError：当数据库的键值出现重复时会出现的错误提示
        db.session.rollback()
        current_app.logger.error(e)
        return  jsonify(errno=RET.DATAEXIST, errmsg=u'用户已存在')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg=u'连接数据库异常')

    # 注册成功并设置session信息
    session['username'] = mobile
    session['mobile'] = mobile
    session['user_id'] = user.id

    # 返回结果
    return jsonify(errno=RET.OK, errmsg="注册成功")

# POST 127.0.0.1:5000/api/v1.0/user/login
@api.route('/user/login',methods=['POST'])
def login():
    """
    Login view
    :return: 0：登录成功，非0：登录失败
    """
    # 接收参数
    data = request.get_json()

    mobile = data.get('mobile')
    password = data.get('password')

    # 校验手机号是否合法
    res = re.match(r"1[3456789]\d{9}",mobile)
    if not res:
        return jsonify(errno=RET.PARAMERR, errmsg=u'手机号不合法')

    # 校验参数
    if not all([mobile,password]):
        return jsonify(errno=RET.NODATA,errmsg=u'数据不完整')

    #判断用户输入的密码错误次数，如果输入5次错误密码 则5分钟后可以继续登录
    user_id = request.remote_addr #获取用户的ip
    try:
        access_count = redis_conn.get('access_nums_%s' %user_id)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_count and access_count == '5':
            return jsonify(errno=RET.REQERR, errmsg=u'密码输入的次数过多，请5分钟后重试')

    # 数据库获取用户
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg=u'数据库连接失败')

    # 校验用户是否存在或者密码是否正确
    if not user or user.check_password(password) is False:
        # 如果输入的用户名或者密码不对，则记录错误次数
        try:
            # redis中的incr会对当前的key对应的value数值+1 ，如果key不存在会将设置key，并且value设置为1
            redis_conn.incr('access_nums_%s' %user_id)
            redis_conn.expire('access_nums_%s' %user_id,300)
        except Exception as e:
            current_app.logger.error(e)
        return jsonify(errno=RET.PWDERR, errmsg=u'用户名或者密码错误')

    # 设置session
    session['username'] = user.name
    session['mobile'] = user.mobile
    session['user_id'] = user.id
    # 返回结果
    return jsonify(errno=RET.OK, errmsg=u'登录成功')


# GET 127.0.0.1:5000/api/v1.0/user/logout
@api.route('/user/logout')
def logout():
    """
    用户退出，删除session
    :return: 0：成功退出 非0：退出失败
    """
    del session['username']
    # session.clear()
    return jsonify(errno=RET.OK, errmsg=u'退出成功')

# GET 127.0.0.1:5000/api/v1.0/user/is_login
@api.route('/user/is_login')
def is_login():
    """
    通过获取session的值来判断用户是否登录 有值 true 无值false
    :return: 0：用户登录 非0：用户未登录
    """
    username = session.get('username','')
    if not username:
        return jsonify(errno=RET.SESSIONERR,errmsg=u'用户未登录')

    return jsonify(errno=RET.OK,data={"username":username})


# POST 127.0.0.1:5000/api/v1.0/user/update_image
@api.route('/user/update_image',methods=['POST'])
@login_required
def update_image():
    """
    参数： 图片(多媒体表单格式)  用户id (g.user_id)
    更用户的头像 用户上传的文件前端接收的文件名称image
    :return: 给前端返回状态信息 及图片的url
    """
    # 接收参数
    file = request.files.get('image')
    # 校验参数
    if not file:
        return jsonify(errno=RET.DATAERR,errmsg=u'上传头像不能为空')
    # 限制用户上传文件的格式
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
    filename = file.filename # 获取上传的文件名称
    if not (filename.rsplit('.')[-1].lower() in ALLOWED_EXTENSIONS and '.' in filename  and \
        secure_filename(filename)):
        return jsonify(errno=RET.DATAERR, errmsg=u'上传的头像不合法')
    # 将客户上传的图片存储到fastdfs
    storage = FDFSStorage(client_conf=current_app.config.get('FDFS_CLIENT_CONF'))
    try:
        file_url = storage.save_file(file.filename,file)
    except Exception as e:
        return jsonify(errno=RET.DATAERR, errmsg=u'上传头像失败')
    # 将图片的url保持的数据中
    user_id = g.user_id # 从g对象中获取user_id
    try:
        User.query.filter_by(id=user_id).update({'avatar_url':file_url})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg=u'保存图片失败')
    
    # 返回消息
    image_url = current_app.config.get('IMAGE_STORAGE_URL') + file_url
    return jsonify(errno=RET.OK, errmsg=u'上传成功', data={'image_url':image_url})


# GET /api/v1.0/user/info
@api.route('/user/info',methods=['GET'])
@login_required
def user_info():
    """
    展示用户头像及用户名信息
    :return: get方式 展示用户的头像信息及用户名
    """
    # 获取用户信息
    user_id = g.user_id # 从g对象中获取user_id login_required装饰器中已经获取到了用户id
    try:
        user = User.query.filter_by(id = user_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg=u'用户信息获取失败')
    # 返回用户信息
    image_url = current_app.config.get('IMAGE_STORAGE_URL') + user.avatar_url
    return jsonify(errno=RET.OK, errmsg=True,data={'username':user.name,'image_url':image_url})

# POST /api/v1.0/user/info
@api.route('/user/info',methods=['POST'])
@login_required
def update_username():
    """
    修改用户
    :return:0：设置成功，并展示目前设置的用户名 非0：设置失败，展示之前的用户名 
    """
    # 获取参数
    data = request.get_json()
    username = data.get('username')
    # 校验参数
    if not username:
        return jsonify(errno=RET.NODATA,errmsg=u'用户名不能为空')
    # 更新数据
    user_id = g.user_id # 获取用户ID
    try:
        user = User.query.filter_by(id=user_id).update({'name':username})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg=u'用户名更新失败')
    # 返回消息
    return jsonify(errno=RET.OK, errmsg=True, data={'username': username})


# GET /api/v1.0/user/user_home
@api.route('/user/user_home')
def user_home():
    """
    个人的home主页
    :return:  展示个人的用户名和手机号及订单详情
    """
    # 如果用户登录 则通过session获取用户的ID 
    user_id = session.get('user_id')
    # 判断用户是否登录
    if not user_id:
        return jsonify(errno=RET.NODATA,errmsg=u'用户未登录')
    # 获取用户的信息
    try:
        user = User.query.filter_by(id=user_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg=u'获取用户信息失败')
    # 返回用户信息 
    return jsonify(errno=RET.OK, errmsg=True,data={'username':user.name,'mobile':user.mobile})