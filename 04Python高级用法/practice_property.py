#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/12 10:42'


# property 类的方法使用
class Money(object):
    def __init__(self):
        self.__money = 0  #定义私有方法，外部无法访问

    def get_money(self):
        return self.__money

    def set_money(self,value):
        if isinstance(value,int):
            self.__money = value
        else:
            print  ('Error: %s is not int' %value)

    money = property(get_money,set_money)

m = Money()
m.money = 10000
print (m.money)


# property 装饰器的使用方式
class Money1(object):
    def __init__(self):
        self.__money = 1

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self,value):
        if isinstance(value,int):
            self.__money = value
        else:
            print ('Error: %s is not int' %value)

    @money.deleter
    def money(self):
        del self.__money


m1 = Money1()
m1.money = 1000000
print (m1.money)