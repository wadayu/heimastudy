#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/8 9:17'


import socket
import re


def service_clinet(client_sock):
    recv_data = client_sock.recv(1024).decode('utf-8')
    # recv_list = recv_data.splitlines()
    # res = re.search(r'/[\w]*(\.html)?',recv_list[0])
    # print (res)

    response = 'HTTP/1.1 200 OK\r\n'
    response += '\r\n'
    response += '<h1>Hello World</h1>'
    client_sock.send(response.encode('utf-8'))
    client_sock.close()


def main():
    # 1 创建套接字
    tcp_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # 2 绑定本地ip port
    tcp_sock.bind(('0.0.0.0',7788))
    # 3 设置被动模式 listen监听状态
    tcp_sock.listen(128)
    while True:
        # 4 等待客户端的连接 accept
        client_sock,clinet_addr = tcp_sock.accept()
        # 5 处理客户端请求
        service_clinet(client_sock)

    # 关闭server端的套接字
    tcp_sock.close()

if __name__ == '__main__':
    main()
