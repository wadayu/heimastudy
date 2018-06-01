#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/1 15:06'

import socket

def main():
    # 1. 创建套接字
    tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 2. 连接服务器
    tcp_socket.connect(('192.168.19.131',7788))

    # 3. 发送文件名
    download_file = input('请输入要下载的文件名：')
    tcp_socket.send(download_file.encode('utf-8'))

    # 4. 接受数据
    recv_data = tcp_socket.recv(1024)

    if recv_data:
        # 5. 将接受的数据写入到本地
        with open('new'+download_file,'wb') as f:
            f.write(recv_data)
        print ('文件[%s]接收成功' %download_file)
    else:
        print('文件[%s]没有找到' % download_file)
        # 6. 关闭套接字
    tcp_socket.close()

if __name__ == '__main__':
    main()