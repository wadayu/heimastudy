#coding:utf-8

import socket

def main():
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udp_socket.bind(('127.0.0.1',7890))
    while True:
        recv_data,recv_addr = udp_socket.recvfrom(1024)
        print ('接收到的内容：%s' %recv_data.decode('utf-8'))
        udp_socket.sendto(b'YES',recv_addr)

if __name__ == '__main__':
    main()