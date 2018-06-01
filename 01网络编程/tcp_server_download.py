#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/1 15:17'

import socket

def main():
    # 1. 创建套接字
    tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 2. 绑定本地IP port
    tcp_socket.bind(('192.168.19.131',7788))

    # 3. 监听客户端
    tcp_socket.listen(128)

    # 4. 应答客户端
    client_socket,client_addr = tcp_socket.accept()

    # 5. 接收要下载的文件名
    file_name = client_socket.recv(1024).decode('utf-8')
    print ('[%s]想要下载: %s' %(client_addr[0],file_name))

    # 6. 读取要下载的文件并发送
    send_data = None
    try:
        f = open(file_name,'rb')
        send_data = f.read()
        f.close()
    except Exception as err:
        print ('抱歉！没有找到：%s' %file_name)

    if send_data:
        client_socket.send(send_data)
        print ('文件[%s]发送成功' %file_name)

    # 7. 关闭套接字
    client_socket.close()
    tcp_socket.close()
if __name__ == '__main__':
    main()