#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/4 15:36'

import multiprocessing
import os


def download_data(q):
    download_list = ['11','22','33','44']

    for i in download_list:
        # 插入数据
        q.put(i)
    print ('download_data over PID:%s' %os.getpid())


def handle_data(q):
    handle = list()
    while True:
        if q.empty(): # 判断q是否为空
            break
            # 获取数据并插入到列表
        handle.append(q.get())
    print (handle)
    print('recve_data over PID:%s' %os.getpid())


def main():

    '''用Queue使两个进程之间的数据共享'''

    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=download_data, args=(q,))
    p2 = multiprocessing.Process(target=handle_data,  args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join() # join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步。
    print ('ok PID:%s' %os.getpid())

if __name__ == '__main__':
    main()
