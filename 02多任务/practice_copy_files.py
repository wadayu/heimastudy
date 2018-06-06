#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/4 17:03'

import os
import multiprocessing


def tasks(q,file_name,old_folder_name,new_folder_name):
    old_f = open(old_folder_name + '/' +file_name,'rb')
    content = old_f.read()
    old_f.close()

    new_f = open(new_folder_name + '/' + file_name, 'wb')
    new_f.write(content)
    new_f.close()

    q.put(file_name)

def main():
    # 获取拷贝的文件夹
    old_folder_name = input('请输入你要拷贝的文件夹： ')

    # 创建新的文件夹
    new_folder_name = old_folder_name + '1'
    try:
        os.mkdir(new_folder_name)
    except Exception as e:
        pass

    # 创建进程池
    po = multiprocessing.Pool(5)

    # 创建队列
    q = multiprocessing.Manager().Queue()

    # 获取将要拷贝的文件
    file_names = os.listdir(old_folder_name)
    for file_name in file_names:
        po.apply_async(tasks,args=(q,file_name,old_folder_name,new_folder_name))

    po.close()

    file_nums = len(file_names)
    copy_ok_nums = 0
    while True:
        print ('%s 拷贝完成' %q.get())
        copy_ok_nums += 1
        print('已经完成%.2f %%' % (copy_ok_nums*100 / file_nums))
        if copy_ok_nums == file_nums:
            break


if __name__ == '__main__':
    main()