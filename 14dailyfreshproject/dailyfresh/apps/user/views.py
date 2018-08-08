from django.shortcuts import render,redirect
from django.views.generic import View
from django.core.urlresolvers import reverse

import re

from user.models import User


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
        if User.objects.filter(username=username):
            return render(request, 'register.html', {'errmsg': '用户已存在'})

        user = User.objects.create_user(username,email,password)
        user.is_active = False
        user.save()

        return redirect(reverse('goods:index'))