#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/20 9:50'

import time


def set_func(func):
    def call_func():
        start_time = time.time()
        func()
        stop_time = time.time()
        print ('运行的时间为%.5f' %(stop_time - start_time))
    return call_func

@set_func
def test():
    print ('Hello World')
    for i in range(1000000):
         pass

# test()

# 装饰器传参数

def set_func_1(func):
    def call_func_1(num):
        print ('验证1')
        func(num)
        print('验证2')
    return  call_func_1

@set_func_1
def test_1(num):
    print ('Hello World---%d' %num)

# test_1(100)

# 不定长度的传参数

def set_func_2(func):
    def call_func_2(*args,**kwargs):
        print ('验证1')
        func(*args,**kwargs)
        print ('验证2')
    return call_func_2

@set_func_2
def test_2(num, *args, **kwargs):
    print('Hello World', num)
    print('Hello World', args)
    print('Hello World', kwargs)

# test_2(100,200,300,name='sb')


# 函数有返回值的装饰器(完整的装饰器)

def set_func_3(func):
    def call_func_3(*args, **kwargs):
        print('验证1')
        print('验证2')
        return  func(*args, **kwargs)
    return  call_func_3

@set_func_3
def test_3(num):
    print('Hello World', num)
    return 'ok'

# res = test_3(102)
# print (res)

# 多个装饰器装饰一个函数

def set_func_4(func):
    def call_func_4(*args, **kwargs):
        return  '<h1>' + func(*args, **kwargs) + '</h1>'
    return  call_func_4


def set_func_5(func):
    def call_func_5(*args, **kwargs):
        return  '<td>' + func(*args, **kwargs) + '</td>'
    return  call_func_5

@set_func_4
@set_func_5
def test_4():
    return 'Hello World'

# print (test_4())


# 带有参数的装饰器


def set_level(level_num):
    def set_func_6(func):
        def call_func_6(*args, **kwargs):
            if level_num == 1:
                print('权限认证1')
            elif level_num == 2:
                print('权限认证2')
            return func(*args, **kwargs)
        return call_func_6
    return set_func_6


@set_level(1)
def test_5():
    print('---test5---')


@set_level(2)
def test_6():
    print('---test6---')

test_5()
test_6()


















