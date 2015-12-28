__author__ = 'liyuan35023'
# -*- coding: utf-8 -*-

import socket
import sys
import argparse

"""套接字创建函数,创建UDP套接字"""
def create_socket():
    try:
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error, e:
        print "Error Creating Socket: %s" % str(e)
        sys.exit(1)
    return send_sock

"""探测包发送函数,暂时只发送单播包"""
def send_packet(sock):
    # 命令行参数解析,从命令行读入目的端ip地址与端口号
    parse = argparse.ArgumentParser(description="Send packet!")
    parse.add_argument("--ip_address", action="store", dest="ip_address", required=True)
    parse.add_argument("--port", action="store", dest="port", type=int, required=True)
    given_args = parse.parse_args()
    ip_address = given_args.ip_address
    port = given_args.port

    # 发送探测包
    packet_info = "This is a test unicast packet."
    try:
        print "Sending Packet..."
        sock.sendto(packet_info, (ip_address, port))
        print "Success to Send packet to %s!" % ip_address
    except socket.error, e:
        print "Error Send Packet: %s" % str(e)
    except Exception, e:
        print "Other Exception: %s" % str(e)
    finally:
        print "Closing connection to the server"
        sock.close()

if __name__ == "__main__":
    sock = create_socket()
    send_packet(sock)

