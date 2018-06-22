#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/19 16:31'

# 什么是闭包？
# 一个函数里面嵌套另外一个函数，而且内部的函数调用外部函数的临时变量，外部函数得到的结果是内部函数的引用，这就叫做闭包！


def outdef(a):
    b = 10
    def indef():
        print (a+b)
    return  indef

out = outdef(5)
out()
