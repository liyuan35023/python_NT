__author__ = 'liyuan35023'
# -*- coding: utf-8 -*-

import socket
import sys
import argparse
import Send_UDPPacket
import ntplib
from time import ctime


"""时间显示函数，用来返回网络时间"""
def getTime():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('cn.ntp.org.cn')
    return ctime(response.tx_time)


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
    parse.add_argument("--ip_address", action="store", dest="ip_address", required=False)
    parse.add_argument("--port", action="store", dest="port", type=int, required=False)
    parse.add_argument("--ptype", action="store", dest="ptype", type=int, required=True)
    given_args = parse.parse_args()
    ip_address = given_args.ip_address
    port = given_args.port
    ptype = given_args.ptype

    ListAddress = [('192.168.1.65', 9999), ('192.168.1.14', 29999)]

    # 探测包内容
    packet_buf = "This is a test unicast packet."
    Packet = Send_UDPPacket.Send_info(getTime(), packet_buf)

    if ptype == 0:
        numberOfpacket = 1
    elif ptype == 1:
        numberOfpacket = 2
    elif ptype == 2:
        numberOfpacket = 3
    else:
        raise ValueError("Wrong Packet Type: %s" % ptype)
    # 发送参数设定
    parameter = Send_UDPPacket.Para_info(ptype, numberOfpacket, len(Packet))

    # 调用单播或者背靠背或者三明治包的类,发送探测包
    print "Sending Packet..."
    if ptype == 0:
        UDPPacket = Send_UDPPacket.SendUnicast()
        UDPPacket.Sendpacket(sock, (ip_address, port), parameter, Packet)
    elif ptype == 1:
        UDPPacket = Send_UDPPacket.SendBackToBack()
        UDPPacket.Sendpacket(sock, ListAddress, parameter, Packet)
    elif ptype == 2:
        UDPPacket = Send_UDPPacket.SendSandwich()
        UDPPacket.Sendpacket(sock, ListAddress, parameter, Packet)

    # UDPPacket = Send_UDPPacket.SendUnicast()
    # UDPPacket.Sendpacket(sock, (ip_address, port), parameter, Packet)
    # print "Success to Send packet to %s!" % ip_address

if __name__ == "__main__":
    sock = create_socket()
    send_packet(sock)

