__author__ = 'liyuan35023'
# -*- coding: utf-8 -*-
"""
该文件已弃用,服务器端使用SocketServer模块实现多进程收包
"""

import socket
import os
from datetime import datetime
from multiprocessing import Process, ProcessError

port = 9999
BUF_SIZE = 1024
address = "127.0.0.1"


"""创建接收UDP套接字"""
def create_socket():
    try:
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error, e:
        print "Error Create recv_Socket: %s" % e
    else:
        # enable reuse address/port
        recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            recv_sock.bind((address, port))
        except socket.error, e:
            print "Error Bind Socket: %s" % e
        else:
            return recv_sock

def receive_packet(sock):
    # 包到达的时间列表,用于计算三明治包的时延
    # arrived_time = []

    while True:
        print "Waiting for data..."
        data, client_addr = sock.recvfrom(BUF_SIZE)
        print "Process %s Received data:'%s' from %s.   Arrived time: %s" % (os.getpid(), data, client_addr, datetime.now())
        #time_now = datetime.now()
        #arrived_time.append(time_now)
        #print time_now
    # print "Closing connection to the server"
    # sock.close()


if __name__ == "__main__":
    print "parent process %s" % (os.getpid())
    sock = create_socket()

    try:
        child_process1 = Process(target=receive_packet, args=(sock, ))
        child_process2 = Process(target=receive_packet, args=(sock, ))
        child_process3 = Process(target=receive_packet, args=(sock, ))
    except ProcessError, e:
        print "Error Create Process: %s" % e
    else:
        try:
            child_process1.start()
            child_process2.start()
            child_process3.start()
        except ProcessError, e:
            print "Error Start Process: %s" % e
        else:
            child_process1.join()
            child_process2.join()
            child_process3.join()

    print "Closing connection to the server"
    sock.close()
