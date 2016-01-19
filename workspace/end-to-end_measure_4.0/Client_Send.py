# -*- coding: utf-8 -*-
__author__ = 'liyuan35023'

import socket
import sys
import Send_UDPPacket
import logging

PORT = 9999

# 定义日志格式,级别,输出位置
logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S', filename='send_err.log', filemode='a')


def create_socket():
    """套接字创建函数,创建UDP套接字"""
    try:
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return send_sock
    except socket.error, e:
        logging.error("Error Creating Socket: %s" % str(e))
        sys.exit(1)


def send_packet(sock):
    """探测包发送函数"""

    # 从文件中读入发送参数,文件的格式为每行代表一个参数,依次为
    # 发送包的类型(单播--0,背靠背--1,三明治--2)
    # 包的数量
    # 发包的时间间隔模式(均匀--0,泊松--1,高斯--2)
    # 发送的包的大小(三明治包中的大包大小为小包的20倍)
    try:
        f_para = open('./readfiles/sendparameter', 'r')
        list_parameter = f_para.readlines()
        while '' in list_parameter:
            list_parameter.remove('')
        if len(list_parameter) != 4:
            logging.error("Miss or unnecessary send parameters in ./readfiles/sendparameter, Need four parameters!")
        else:
            ptype = int(list_parameter[0].strip())   # strip把行尾'\n'字符去掉
            nPacket = int(list_parameter[1].strip())
            interval_mode = int(list_parameter[2].strip())
            psize = int(list_parameter[3].strip())
    except IOError, e:
        logging.error("can't open './readfiles/sendparameter' : %s" % e)
        raise IOError("can't open './readfiles/sendparameter' : %s" % e)
    finally:
        if f_para:
            f_para.close()

    # ListAddress代表目的地址,从文件读入ip,默认PORT为9999
    ListAddress = []
    if ptype == 0:
        with open('./readfiles/Unicast_ip', 'r') as f_Unicast:
            for line in f_Unicast.readlines():
                if line.strip() and (line.strip() != socket.gethostname()):    # 行不为空
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
        logging.error("Unexpected Packet Type %s" % ptype)  # logging.exception
        raise ValueError("Unexpected Packet Type %s" % ptype)

    try:
        # 发送参数设定
        parameter = Send_UDPPacket.Para_info(ptype, interval_mode, psize, nPacket)
    except Exception, e:
        logging.error("Error generate Para info, may be file 'sendparameter' is not be read successfully: %s" % e)
    else:
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
            logging.error("Packet Type %s Not Found" % ptype)
            raise ValueError("Packet Type %s Not Found" % ptype)


# 主函数,在measure_tools中调用main函数
def main():
    sock = create_socket()
    send_packet(sock)

if __name__ == "__main__":
    main()
