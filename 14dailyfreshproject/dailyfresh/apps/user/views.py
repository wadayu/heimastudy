from django.shortcuts import render,redirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse,JsonResponse
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection

import re
# 对数据进行加密 （pip install itsdangerous）
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from itsdangerous import SignatureExpired # 过期异常
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from celery_tasks.tasks import send_register_email,send_update_email
from utils.mixin import LoginRequiredMixin
from user.models import User,Address
from goods.models import GoodsSKU
from order.models import OrderInfo,OrderGoods


# /register
class RegisterView(View):
    # 注册View
    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 用户输入的内容校验是否为空
        if not all([username,password,email]):
            return render(request,'register.html',{'errmsg':'数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        # 校验是否同意协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请先同意协议'})

        # 校验用户是否存在
        if User.objects.filter(Q(username=username)|Q(email=username)):
            return render(request, 'register.html', {'errmsg': '用户已存在或者邮箱已经注册'})

        user = User.objects.create_user(username,email,password)
        user.is_active = False
        user.save()

        # 对用户身份信息进行加密
        s = serializer(settings.SECRET_KEY,300)
        info = {'user_id':user.id}
        token = s.dumps(info)
        token = token.decode('utf-8')


        # 发送激活用户邮件
        send_register_email.delay(username,email,token) # celery 异步

        email_name = re.split('@|\.',email)[1]
        return render(request,'register_success.html',{'name':email_name})


# /user/active/token
class ActiveView(View):
    # 用户激活view
    def get(self,request,token):
        try:
            s = serializer(settings.SECRET_KEY, 300)
            info = s.loads(token)
            user_id = info['user_id']
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()

            return  redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('激活已过期')
        except Exception as e:
            return render(request,'404.html')

# /user/login
class LoginView(View):
    # 用户登录
    def get(self,request):
        # 判断是否记住用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request,'login.html',{'username': username,'checked': checked})

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        remember = request.POST.get('remember')

        # 判断用户名或者密码为空
        if not all([username,password]):
            return render(request, 'login.html', {'errmsg': "数据不完整"})

        # 通过邮箱登录验证
        pattern = '^\w{6,15}\@[a-z0-9]+(\.[0-9a-z]+){1,2}$'
        if re.match(pattern,username):
            try:
                user = User.objects.get(email=username)
                username = user.username
            except Exception as e:
                return render(request, 'login.html', {'errmsg': "用户未注册"})

        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)

                # 获取登录后所要跳转到的地址
                # 默认跳转到首页
                # http://127.0.0.1:8000/user/login/?next=/user/info/
                # 当用户未登录要访问个人中心时，会跳到此页面（要在settings里配置登录的地址LOGIN_URL = '/user/login/'）
                # 当用户成功登录时，会自动跳转到next后面的url
                next_url = request.GET.get('next',reverse('goods:index'))
                response = redirect(next_url)
                # 是否记住用户名
                if remember == 'on':
                    response.set_cookie('username',username,max_age=7*24*3600)
                else:
                    response.delete_cookie('username')

                return response
            else:
                return render(request, 'login.html', {'errmsg': "用户未激活"})
        else:
            return render(request,'login.html',{'errmsg':"用户名或者密码错误"})

# /user/update_pwd
class UpdatePwdView(View):
    # 找回密码页面
    def get(self,request):
        return render(request,'update_pwd.html')

    def post(self,request):
        res = request.POST
        username = res['username']

        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            email = user.email

            # 对用户身份信息进行加密
            s = serializer(settings.SECRET_KEY, 300)
            info = {'user_id': user.id}
            token = s.dumps(info)
            token = token.decode('utf-8')

            # 发送找回用户邮件
            send_update_email.delay(email, token)  # celery 异步

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'fail'})


class ModifyPwdView(View):
    # 用户输入新密码
    def get(self,request,token):
        try:
            s = serializer(settings.SECRET_KEY, 300)
            info = s.loads(token)
            user_id = info['user_id']
            user = User.objects.get(id=user_id)

            return  render(request,'reset_pwd.html',{'username':user})
        except SignatureExpired as e:
            return HttpResponse('验证码已过期')
        except Exception as e:
            return render(request,'404.html')

class ResetPwdView(View):
    # 重设密码
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        user = User.objects.get(username=username)
        user.password = make_password(password)
        user.save()

        return redirect(reverse('user:login'))

# /user/logout
class LogoutView(View):
    # 退出登录
    def get(self,request):
        logout(request)
        return redirect(reverse('goods:index'))


# /user/info
class UserInfoView(LoginRequiredMixin,View):
    # 个人中心
    def get(self,request):
        # 获取redis的对象
        con = get_redis_connection('default')
        # 标记用户浏览记录的key
        history_key = 'history_%s' %request.user.id
        # 获取用户最近的5次商品浏览记录
        sku_ids = con.lrange(history_key,0,4)

        # 根据商品的id获取商品详情信息
        goods_li = []
        for good_id in sku_ids:
            try:
                good = GoodsSKU.objects.get(id=int(good_id))
                goods_li.append(good)
            except GoodsSKU.DoesNotExist as e:
                # 找不到good_id对应的商品，就删除对应的浏览记录
                con.lrem(history_key,0,good_id) # lrem 删除redis list内的对应值

        # 获取默认收货地址
        address = Address.objects.get_default_address(user=request.user)

        context = {'page': 'info',
                   'address': address,
                   'goods_li':goods_li}

        return render(request,'user_center_info.html',context)

# /user/order
class UserOrderView(LoginRequiredMixin,View):
    # 个人订单
    def get(self,request):
        user = request.user
        # 用户的所有订单信息
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')
        order_status = {1: '待支付',2:'待发货',3:'待收货',4:'待评价',5:'已完成'}
        for order in orders:
            # 订单内的所有商品
            all_goods = OrderGoods.objects.filter(order=order.order_id)
            for good in all_goods:
                # 计算商品的小计
                amount = good.price * good.count
                # 动态给商品增加小计价格
                good.amount = amount
            # 动态给订单增加订单内的所有商品信息
            order.all_goods = all_goods
            order.status = order_status[order.order_status]

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(orders, 2, request=request)
        all_orders = p.page(page)

        context = {
            'page':'order',
            'orders':all_orders
        }
        return render(request,'user_center_order.html',context)


# /user/address
class UserAddressView(LoginRequiredMixin,View):
    # 个人收货地址
    def get(self,request):
        page = 'address'
        all_address = Address.objects.filter(user=request.user)
        return render(request,'user_center_site.html',{'page':page,'all_address':all_address})

    def post(self,request):
        receiver = request.POST.get('receiver')
        address = request.POST.get('address')
        code = request.POST.get('code')
        phone = request.POST.get('phone')

        status = Address.objects.create(user=request.user,receiver=receiver,addr=address,zip_code=code,phone=phone)

        if status:
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status': 'fail'})


# /user/update_address
class UpdateDefaultAddressView(View):
    # 更新默认收货地址 删除收货地址
    def post(self,request):
        type = request.POST.get('type')
        address_id = request.POST.get('addr_id')

        if type == '默认':
            # 查找默认的收货地址 并取消默认
            def_address = Address.objects.filter(user=request.user,is_default=True)
            for address in def_address:
                address.is_default = False
                address.save()

            # 添加新的默认地址
            new_def = Address.objects.get(id=int(address_id))
            new_def.is_default = True
            new_def.save()

            return JsonResponse({'status': 'success'})
        else:
            Address.objects.get(id=int(address_id)).delete()
            return JsonResponse({'status': 'delete_success'})

class UserCommentView(LoginRequiredMixin,View):
    """用户的所有评论"""
    def get(self,request):
        orders = OrderInfo.objects.filter(user=request.user).order_by('-create_time')
        for order in orders:
            all_goods = OrderGoods.objects.filter(order=order)
            for good in all_goods:
                amount = good.price * good.count
                good.amount = amount
            order.all_goods = all_goods

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(orders, 2, request=request)
        all_orders = p.page(page)

        context = {
            'page':'comment',
            'all_orders':all_orders
        }
        return render(request,'user_center_comment.html',context)



