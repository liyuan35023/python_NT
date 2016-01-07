__author__ = 'liyuan35023'
# -*- coding: utf-8 -*-

import socket
import sys
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

    # 从文件中读入发送参数,文件的格式为每行代表一个参数,依次为
    # 发送包的类型(单播--0,背靠背--1,三明治--2)
    # 包的数量
    # 发包的时间间隔模式(均匀--0,泊松--1,高斯--2)
    # 发送的包的大小(三明治包中的大包大小为小包的20倍)
    with open('./readfiles/sendparameter', 'r') as f_para:
        list_parameter = f_para.readlines()
        while '' in list_parameter:
            list_parameter.remove('')
        if len(list_parameter) != 4:
            raise ValueError("Miss send parameters in ./readfiles/sendparameter.txt, Need four parameters!")
        else:
            ptype = int(list_parameter[0].strip())   ## strip把行尾'\n'字符去掉
            nPacket = int(list_parameter[1].strip())
            interval_mode = int(list_parameter[2].strip())
            psize = int(list_parameter[3].strip())

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


# 主函数,在measure_tools中调用main函数
def main():
    sock = create_socket()
    send_packet(sock)

if __name__ == "__main__":
    main()