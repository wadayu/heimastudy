#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/1 18:13'


import threading
import time


class MyThread(threading.Thread):

    def run(self):
        self.saysorry()
        self.sayloveme()
        print(threading.enumerate())

    def saysorry(self):
        for i in range(5):
            print ('我错了，我真的错了！')
            time.sleep(1)

    def sayloveme(self):
        for i in range(5):
            print ('我爱你，我真的爱你！')
            time.sleep(1)


if __name__ == '__main__':
    t = MyThread()
    t.start()
