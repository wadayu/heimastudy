#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/4 15:36'

import multiprocessing


def download_data(q):
    download_list = ['11','22','33','44']
    for i in download_list:
        # 插入数据
        q.put(i)


def handle_data(q):
    handle = list()
    while True:
        if q.empty(): # 判断q是否为空
            break
        # 获取数据并插入到列表
        handle.append(q.get())
    print (handle)


def main():

    '''用Queue使两个进程之间的数据共享'''

    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=download_data, args=(q,))
    p2 = multiprocessing.Process(target=handle_data,  args=(q,))
    p1.start()
    p2.start()

if __name__ == '__main__':
    main()