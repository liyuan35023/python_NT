__author__ = 'liyuan35023'
# -*- coding: utf-8 -*-

import socket
import sys
import argparse
import Send_UDPPacket

PORT = 9999

"""套接字创建函数,创建UDP套接字"""
def create_socket():
    try:
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error, e:
        print "Error Creating Socket: %s" % str(e)
        sys.exit(1)
    return send_sock

"""探测包发送函数"""
def send_packet(sock):
    # 命令行参数解析,从命令行读入发包类型,发包数量,发包的间隔模式(均匀,泊松,正态),小包大小
    parse = argparse.ArgumentParser(description="Send packet!")
    parse.add_argument("--ptype", action="store", dest="ptype", type=int, required=True)
    parse.add_argument("--nPacket", action="store", dest="nPacket", type=int, required=False)
    parse.add_argument("--interval_mode", action="store", dest="interval_mode", type=int, required=True)
    parse.add_argument("--psize", action="store", dest="psize", type=int, required=True)
    given_args = parse.parse_args()
    ptype = given_args.ptype
    nPacket = given_args.nPacket
    interval_mode = given_args.interval_mode
    psize = given_args.psize

    # ListAddress代表目的地址,从文件读入ip,默认PORT为9999
    ListAddress = []
    if ptype == 0:
        with open('./readfiles/Unicast_ip', 'r') as f_Unicast:
            for line in f_Unicast.readlines():
                if line.strip():    # 行不为空
                    ListAddress.append((line.strip(), PORT))   # strip把行尾'\n'字符去掉
    elif ptype == 1:
        with open('./readfiles/BackToBack_ip', 'r') as f_BackToBack:
            for line in f_BackToBack.readlines():
                if line.strip():    # 行不为空
                    ListAddress.append((line.strip(), PORT))
    elif ptype == 2:
        with open('./readfiles/Sandwich_ip', 'r') as f_Sandwich:
            for line in f_Sandwich.readlines():
                if line.strip():    # 行不为空
                    ListAddress.append((line.strip(), PORT))
    else:
        raise ValueError("Packet Type %s Not Found" % ptype)

    # 发送参数设定
    parameter = Send_UDPPacket.Para_info(ptype, interval_mode, psize, nPacket)

    # 调用单播或者背靠背或者三明治包的类,发送探测包
    print "Sending Packet..."
    if ptype == 0:
        UDPPacket = Send_UDPPacket.SendUnicast()
        UDPPacket.Sendpacket(sock, ListAddress, parameter)
    elif ptype == 1:
        UDPPacket = Send_UDPPacket.SendBackToBack()
        UDPPacket.Sendpacket(sock, ListAddress, parameter)
    elif ptype == 2:
        UDPPacket = Send_UDPPacket.SendSandwich()
        UDPPacket.Sendpacket(sock, ListAddress, parameter)
    else:
        raise ValueError("Packet Type %s Not Found" % ptype)

if __name__ == "__main__":
    sock = create_socket()
    send_packet(sock)

