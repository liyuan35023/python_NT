__author__ = 'liyuan35023'
# -*- coding: utf-8 -*-

import socket
import sys

port = 9999
BUF_SIZE = 1024
address = "127.0.0.1"

"""创建接收UDP套接字"""
def create_socket():
    try:
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error, e:
        print "Error Create recv_Socket: %s" % e
    # enable reuse address/port
    recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #address=socket.gethostbyname(socket.gethostname())
    try:
        recv_sock.bind((address, port))
    except socket.error, e:
        print "Error Bind Socket: %s" % e
    return recv_sock

def receive_packet(sock):
    while True:
        print "Wating for data..."
        data, client_addr = sock.recvfrom(BUF_SIZE)
        print "Received data:'%s' from %s" % (data, client_addr)
    print "Closing connection to the server"
    sock.close()


if __name__ == "__main__":
    sock = create_socket()
    receive_packet(sock)
