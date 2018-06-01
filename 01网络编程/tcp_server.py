#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/1 10:55'

import socket

def main():
    # 1 创建套接字
    tcp_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # 2 绑定本地ip port
    tcp_sock.bind(('192.168.19.131',7788))
    # 3 设置被动模式 listen监听状态
    tcp_sock.listen(128)
    while True:
        # 4 等待客户端的连接 accept
        print('等待新的客户连接。。。。')
        client_sock,clinet_addr = tcp_sock.accept()
        while True:
            # 5 接收消息
            recv_data = client_sock.recv(1024)
            print ('客户发送过来的消息： %s' %recv_data.decode('utf-8'))
            if recv_data.decode('utf-8') == 'exit':
                break
            elif recv_data.decode('utf-8') == '':
                break
            # 6 发送消息
            client_sock.send('Yes!'.encode('utf-8'))

        # 6 关闭套接字
        client_sock.close()
    # 关闭server端的套接字
    clinet_soct.close()

if __name__ == '__main__':
    main()
