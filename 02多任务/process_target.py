#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/4 14:36'

import time
import multiprocessing

def sing():
    while True:
        print ("I'm singing Fadad")
        time.sleep(1)


def dance():
    while True:
        print ("I'm danceing JieWu")
        time.sleep(1)


def main():
    p1 = multiprocessing.Process(target=sing)
    p2 = multiprocessing.Process(target=dance)
    p1.start()
    p2.start()

if __name__ == '__main__':
    main()