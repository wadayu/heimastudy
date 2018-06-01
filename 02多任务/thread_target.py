#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/1 17:58'

import time
import threading

'''线程运行没有顺序的'''

def sing():
    for i in range(5):
        print ("I'm singing Fadad ---%d---" %i)
        time.sleep(1)


def dance():
    for i in range(5):
        print ("I'm danceing JieWu ---%d---" %i)
        time.sleep(1)

def main():
    t1 = threading.Thread(target=sing)
    t2 = threading.Thread(target=dance)

    t1.start()
    t2.start()

    # 查看运行的线程
    print (threading.enumerate())

if __name__ == '__main__':
    main()