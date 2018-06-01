#coding:utf-8

import socket

def main():
    # 1 创建套接字
    tcp_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # 2 创建连接
    tcp_sock.connect(('192.168.19.131',7788))
    while True:
        # 3 接收发送消息
        send_data = input('请输入你想发送的内容： ')
        tcp_sock.send(send_data.encode('utf-8'))
        if send_data == 'exit' or not send_data:
            break

        recv_data = tcp_sock.recv(1024)
        print (recv_data.decode('utf-8'))
    # 4 关闭套接字
    tcp_sock.close()

if __name__ == '__main__':
    main()
