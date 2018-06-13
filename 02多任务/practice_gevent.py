#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/5 17:39'

'''协程练习'''

from gevent import monkey
import gevent
import time

monkey.patch_all() # 将所有阻塞（比如：time.sleep）转换为gevent.time


def tasks(args_name):
    for i in range(5):
        print ('---%s---,%d' %(args_name,i))
        time.sleep(0.5)


def main():
    gevent.joinall([
        gevent.spawn(tasks, 'work1'),
        gevent.spawn(tasks, 'work2')
    ])

# def main():
#     L = ('work1', 'work2', 'work3')
#     gevent.joinall([
#         gevent.spawn(tasks, i) for i in L
#     ])

    '''
        gevent.joinall([                            
        gevent.spawn(tasks, 'work1'),
        gevent.spawn(tasks, 'work2')
    ])
    ====等价于下面内容
    g1 = gevent.spawn(tasks,'work1')
    g2 = gevent.spawn(tasks,'work2')
    g1.join()
    g2.join()
    '''

if __name__ == '__main__':
    main()