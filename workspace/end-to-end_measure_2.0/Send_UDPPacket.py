__author__ = 'liyuan35023'
# -*- coding: utf-8 -*-

import socket

typeUnicast = 0
typeBacktoBack = 1
typeSandwich = 2

# 探测包信息类,包括发送的时间,发送的字符串信息
class Send_info(object):
    def __init__(self, SendTime, packet_buf):
        self.__SendTime = SendTime
        self.__packet_buf = packet_buf
    def __str__(self):
        send_str = str(self.__SendTime) + str(self.__packet_buf)
        return send_str
    def __len__(self):
        return len(str(self.__SendTime) + str(self.__packet_buf))


# 发送参数类,包括发送包的类型,包的数量(指的是整个包的数量,比如共有2个背靠背包,指两个目的结点各收到两个包)，
# 包的间隔（同包的数量的解释）
class Para_info(object):
    def __init__(self, packet_type, packet_size, nPacket=1, packet_interval=0):
        self.packet_type = packet_type
        self.packet_size = packet_size
        self.nPacket = nPacket
        self.packet_interval = packet_interval


"""该类用来执行客户端的发送命令,是一个基类."""
"""可用于发送单播,背靠背包或三明治包"""
class UDPSend(object):
    def Sendpacket(self, sock, (addr,port), para_infomation, sendpacket_info):
        pass

"""单播包发送类,继承发送基类(Version2.1:可以连续发送单播包)"""
class SendUnicast(UDPSend):
    def Sendpacket(self, sock, (addr, port), para_infomation, sendpacket_info):
        if para_infomation.packet_type != typeUnicast:
            raise ValueError("Wrong Packet Type: %s" % para_infomation.packet_type)
        packet_count = 1     # 包计数器
        while True:
            try:
                sock.sendto(str(sendpacket_info), (addr, port))
                print "Success to Send Num %s Unicast packet to %s!" % (packet_count, addr)
            except socket.error, e:
                print "Error Send Num %s Unicast Packet: %s" % (packet_count, str(e))
            except Exception, e:
                print "Other Exception When sending Num %s Unicast Packet: %s" % (packet_count, str(e))
            packet_count += 1
            if packet_count > para_infomation.nPacket:
                break         #当包计数器超过预先设定的发包数时,退出循环
        print "Closing Connection to the Server..."
        sock.close()
`   refrea

"""背靠背包发送类,继承发送基类"""
class SendBackToBack(UDPSend):
    def Sendpacket(self, sock, ListAddress, para_infomation, sendpacket_info):
        if para_infomation.packet_type != typeBacktoBack:
            raise ValueError("Wrong Packet Type: %s" % para_infomation.packet_type)
        for (addr, port) in ListAddress:
            try:
                sock.sendto(str(sendpacket_info), (addr, port))
                print "Success to Send BTB Packet to %s!" % addr
            except socket.error, e:
                print "Error Send BTB Packet to %s: %s" % (addr, str(e))
            except Exception, e:
                print "Other Exception: %s" % str(e)
        print "Closing Connection to the Server..."
        sock.close()

"""三明治包发送类,继承发送基类"""
class SendSandwich(UDPSend):
    def Sendpacket(self, sock, ListAddress, para_infomation, sendpacket_info):
        if para_infomation.packet_type != typeSandwich:
            raise ValueError("Wrong Packet Type: %s" % para_infomation.packet_type)
        # 向目的结点1发送第一个小探测包
        try:
            sock.sendto(str(sendpacket_info), ListAddress[0])
            print "Success to Send first small sandwich packet to %s" % ListAddress[0][0]
        except socket.error, e:
            print "Error to Send first small sanwich packet to %s: %s" % (ListAddress[0][0], str(e))
        except Exception, e:
            print "Other Exception: %s" % str(e)

        # 向目的结点2发送第二个大探测包
        try:
            sock.sendto(str(sendpacket_info), ListAddress[1])
            print "Success to Send second large sandwich packet to %s" % ListAddress[1][0]
        except socket.error, e:
            print "Error to Send second large sanwich packet to %s: %s" % (ListAddress[1][0], str(e))
        except Exception, e:
            print "Other Exception: %s" % str(e)

        # 向目的结点1发送第二个小探测包
        try:
            sock.sendto(str(sendpacket_info), ListAddress[0])
            print "Success to Send third small sandwich packet to %s" % ListAddress[0][0]
        except socket.error, e:
            print "Error to Send third small sanwich packet to %s: %s" % (ListAddress[0][0], str(e))
        except Exception, e:
            print "Other Exception: %s" % str(e)

        print "Closing Connection to the Server..."
        sock.close()