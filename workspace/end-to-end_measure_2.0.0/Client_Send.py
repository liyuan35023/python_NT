# -*- coding: utf-8 -*-
__author__ = 'liyuan35023'

"""
该文件为测量模块的发送子模块,运行在测量节点上

Fuction:
create_socket()---创建UDP套接字
read_sendparameter()---读取发送参数配置文件
measure_matrix_read()---读取测量矩阵,返回目的地址列表]
send_packet()---发送探测包
main()---主函数
"""

import sys
import os.path
import socket
import Send_UDPPacket
import logging
import linecache


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


def read_sendparameter():
    """从文件中读入发送参数,包括发包类型,发包数量,发包间隔模式,包的大小,并返回
    文件的格式为每行代表一个参数,依次为
    ---发送包的类型(单播--0,背靠背--1,三明治--2)
    ---包的数量
    ---发包的时间间隔模式(均匀--0,泊松--1,高斯--2)
    ---发送的包的大小(三明治包中的大包大小为小包的20倍)"""
    try:
        file_para = open('./readfiles/sendparameter', 'r')
        list_parameter = file_para.readlines()
        while '' in list_parameter:
            list_parameter.remove('')       # 删除配置文件中的空行
        if len(list_parameter) != 4:
            logging.error("Miss or unnecessary send parameters in ./readfiles/sendparameter, Need four parameters!")
        # ptype = int(list_parameter[0].strip())   # strip把行尾'\n'字符去掉
        # nPacket = int(list_parameter[1].strip())
        # interval_mode = int(list_parameter[2].strip())
        # psize = int(list_parameter[3].strip())
    except IOError, e:
        logging.error("read sendparameter './readfiles/sendparameter' error : %s" % e)
        raise IOError("read sendparameter './readfiles/sendparameter' error : %s" % e)
    else:
        return map(int, list_parameter)          # 返回参数list
    finally:
        if 'file_para' in locals():    # 如果文件打开成功,则关闭.若打开成功,则关闭.避免Local variable ...错误
            file_para.close()


def measure_matrix_read():
    """测量矩阵读入函数(只用于单播包!!)
    读入测量矩阵,生成目的地址列表并返回"""
    # ListAddress代表目的地址,从测量矩阵读入ip,默认PORT为9999
    ListAddress = []
    # node字典,每个PlanetLab节点对应一个序号
    node_dict = {'abc': 1, 'qwe': 2, 'xyz': 3, 'asd': 4}
    # 序号字典,node字典的反字典
    sequence_dict = {1: 'abc', 2: 'qwe', 3: 'xyz', 4: 'asd'}
    # 得到本节点对应的序号
    sequence = node_dict.get(socket.gethostname())

    # 从文件中读入节点对应的行
    linecache.clearcache()
    if os.path.isfile('./readfiles/measure_matrix'):
        # 读入行,转换为int类型,存入sequence_list中.
        sequence_list = map(int, linecache.getline('./readfiles/measure_matrix', sequence).strip().split(' '))
    else:
        logging.error("measure_matrix is not found")
        raise IOError("measure_matrix is not found")
    for index, item in enumerate(sequence_list):
        # 1代表本节点为源节点,-1代表本节点为目的节点.0代表两个节点间不存在测量路径
        if item == 1:
            # 读取序列字典,将序号对应的节点的hostname存入ListAddress中.
            ListAddress.append((sequence_dict.get(index+1), PORT))
    return ListAddress


def send_packet(sock, para_list, address_list):
    """探测包发送函数"""

    # # ListAddress代表目的地址,从文件读入ip,默认PORT为9999
    # ListAddress = []
    # if ptype == 0:
    #     with open('./readfiles/Unicast_ip', 'r') as f_Unicast:
    #         for line in f_Unicast.readlines():
    #             if line.strip() and (line.strip() != socket.gethostname()):    # 行不为空
    #                 ListAddress.append((line.strip(), PORT))   # strip把行尾'\n'字符去掉
    # elif ptype == 1:
    #     with open('./readfiles/BackToBack_ip', 'r') as f_BackToBack:
    #         for line in f_BackToBack.readlines():
    #             if line.strip():    # 行不为空
    #                 ListAddress.append((line.strip(), PORT))
    # elif ptype == 2:
    #     with open('./readfiles/Sandwich_ip', 'r') as f_Sandwich:
    #         for line in f_Sandwich.readlines():
    #             if line.strip():    # 行不为空
    #                 ListAddress.append((line.strip(), PORT))
    # else:
    #     logging.error("Unexpected Packet Type %s" % ptype)  # logging.exception
    #     raise ValueError("Unexpected Packet Type %s" % ptype)
    try:
        # 发送参数设定
        parameter = Send_UDPPacket.Para_info(para_list[0], para_list[2], para_list[3], para_list[1])
    except Exception, e:
        logging.error("Error generate Para info, may be file 'sendparameter' is not be read successfully: %s" % e)
    else:
        # 调用单播或者背靠背或者三明治包的类,发送探测包
        print "Sending Packet..."
        if parameter.packet_type == 0:
            UDPPacket = Send_UDPPacket.SendUnicast()
            UDPPacket.Sendpacket(sock, address_list, parameter)
        elif parameter.packet_type == 1:
            UDPPacket = Send_UDPPacket.SendBackToBack()
            UDPPacket.Sendpacket(sock, address_list, parameter)
        elif parameter.packet_type == 2:
            UDPPacket = Send_UDPPacket.SendSandwich()
            UDPPacket.Sendpacket(sock, address_list, parameter)
        else:
            logging.error("Packet Type %s Not Found" % parameter.packet_type)
            raise ValueError("Packet Type %s Not Found" % parameter.packet_type)


# 主函数,在measure_tools中调用main函数
def main():
    sock = create_socket()
    para_list = read_sendparameter()
    address_list = measure_matrix_read()
    send_packet(sock, para_list, address_list)

if __name__ == "__main__":
    main()
