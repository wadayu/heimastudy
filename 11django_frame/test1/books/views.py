from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.conf import settings
# 分页功能
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from .models import HeroInfo,UploadPic,AreaInfo

import time



def loginRequire(func):
    """登录验证"""
    def wrapper(request,*args,**kwargs):
        if not request.session.has_key('islogin'):
            return HttpResponseRedirect('/login_session')
        else:
            return func(request,*args,**kwargs)
    return wrapper


def index(request):
    """首页登录页面"""
    return render(request,'books/index.html',{})


def login(request):
    """用户登录页面"""
    return render(request,'books/login.html',{})

# check_pass
def check_pass(request):
    """ajax登录密码验证"""
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username == 'admin' and password == 'admin':
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({'res': 0})

#login_cookie
def login_cookie(request):
    username = request.COOKIES.get('username')
    return render(request,'books/login_cookie.html',{'username':username})

#check_cookie  密码验证
def check_cookie(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')

    if username == 'admin' and password == 'admin':
        response = HttpResponseRedirect('/index')
        # 是否记住用户名 on记住
        if remember == 'on':
            response.set_cookie('username',username,max_age=7*24*3600) # 过期时间1周
        return response
    else:
        return HttpResponseRedirect('/login_cookie')

# login_session
def login_session(request):
    """登录"""
    username = request.COOKIES.get('username')

    if not request.session.has_key('islogin'):
        return render(request, 'books/login_session.html', {'username':username})
    else:
        return render(request, 'books/change_pwd.html', {})


# check_session
def check_session(request):
    """密码验证"""
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')

    verify1 = request.POST.get('verify')
    verify2 = request.session.get('verifycode')
    if verify1.lower() != verify2.lower():
        return HttpResponseRedirect('/login_session')

    if username == 'admin' and password == 'admin':
        response = HttpResponseRedirect('/change_pwd')
        if remember == 'on':  # 是否记住用户名
            response.set_cookie('username',username,max_age=7*24*3600) # 设置cookie

        request.session['islogin'] = True  # 设置session登录状态
        return response
    else:
        return HttpResponseRedirect('/login_session')
    
@loginRequire
def change_pwd(request):
    """修改密码页面"""
    return render(request,'books/change_pwd.html')

@loginRequire
def change_pwd_ation(request):
    """修改密码的状态页面"""
    return HttpResponse('修改成功')
    
# url template_vars 模板变量
def template_vars(request):
    my_list = [[1,2,3],['a','b','c']]
    list_count = list(range(1,10))
    heros = HeroInfo.objects.all()
    return render(request,'books/template_vars.html',{'my_list': my_list, 
                                                      'list_count': list_count,
                                                      'heros':heros,})

from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO

# 验证码

# /verify_code
def verify_code(request):
    """验证码函数"""
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高 RGB
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)

    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]

    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('Candarai.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')



# 用户上传图片处理

def upload_show(request):
    return render(request,'books/upload_image.html')

def uplaod_handle(request):
    # 1、获取图片对象
    pic = request.FILES.get('pic')
    # 2、保存图片文件
    now_time = time.strftime('%Y%m%d')
    save_path = '%s/books/%s/%s' %(settings.MEDIA_ROOT,now_time,pic.name)
    with open(save_path,'wb') as f:
        for content in pic.chunks():
            f.write(content)
    # pic.chunks() 保存的图片的数据 是一个生成器 # 迭代整个文件，并生成指定大小的一部分内容。chunk_size默认为64KB。
    # 3、保存到数据库
    UploadPic.objects.create(path='books/%s/%s' %(now_time,pic.name))
    # 4、返回响应
    return HttpResponse('上传成功！')

# 地区详情信息
def area_info(request):
    return render(request,'books/area_info.html')

# 获取省份的view

def get_prov(request):
    # 获取省级地区
    all_prov = AreaInfo.objects.filter(pid__isnull=True)

    all_prov_list = []
    for prov in all_prov:
        all_prov_list.append((prov.id,prov.atitle))

    return JsonResponse({'areas':all_prov_list})


def get_city(request,area_id):
    # 获取省份的下级市
    all_city = AreaInfo.objects.filter(pid__id=int(area_id))
    
    all_city_list = []
    for city in all_city:
        all_city_list.append((city.id,city.atitle))
        
    return JsonResponse({'city':all_city_list})


def get_county(request, city_id):
    # 获取市级下面的县
    all_county = AreaInfo.objects.filter(pid__id=int(city_id))

    all_county_list = []
    for city in all_county:
        all_county_list.append((city.id, city.atitle))

    return JsonResponse({'county': all_county_list})

def get_info(request):
    # 获取提交的详细信息
    prov_id = request.POST.get('prov')
    city_id = request.POST.get('city')
    county_id = request.POST.get('county')
    address = request.POST.get('address')
    prov = AreaInfo.objects.get(id=int(prov_id))
    city = AreaInfo.objects.get(id=int(city_id))
    county = AreaInfo.objects.get(id=int(county_id))
    info = prov,city,county,address
    return HttpResponse(info)


# 分页
def get_areas(request):
    all_areas = AreaInfo.objects.filter(pid__isnull=True)

    # 分页
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(all_areas, 2, request=request)
    areas = p.page(page)

    return render(request,'books/areas.html',{'all_areas':areas})