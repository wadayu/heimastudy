#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/4 11:43'

import threading

global_num = 0
thread_look = threading.Lock()

def test1(loop_num):
    global global_num
    thread_look.acquire()
    for i in range(loop_num):
        global_num += 1
    thread_look.release()
    print ('test1---%d---' %global_num)


def test2(loop_num):
    global global_num
    thread_look.acquire()
    for i in range(loop_num):
        global_num += 1
    thread_look.release()
    print('test2---%d---' % global_num)


def main():
    t1 = threading.Thread(target=test1, args=(1000000,))
    t2 = threading.Thread(target=test2, args=(1000000,))
    t1.start()
    t2.start()
    print('test---%d---' % global_num)

if __name__ == '__main__':
    main()