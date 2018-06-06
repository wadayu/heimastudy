#coding:utf-8

import socket

def main():
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    while True:
        send_data = input('请输入你要发送的内容: ')
        udp_socket.sendto(send_data.encode('utf-8'),('127.0.0.1',7890))

        recv_data,recv_addr = udp_socket.recvfrom(1024)
        print (recv_data.decode('utf-8'))

if __name__ == '__main__':
    main()