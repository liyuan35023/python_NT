__author__ = 'liyuan35023'
# -*- coding: utf-8 -*-

import socket
import random
import string
import ntplib
import threading
from multiprocessing import Process, Event
from time import ctime, sleep
from datetime import datetime
from scipy import stats

# 发送包的类型
TYPE_UNICAST = 0
TYPE_BACKTOBACK = 1
TYPE_SANDWICH = 2

# 发送包时间间隔模式
UNIFORM = 0
POISSON = 1
GAUSS = 2


"""时间显示函数,用来返回网络时间"""
def get_time():
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('cn.ntp.org.cn')
    except socket.gaierror:
        sleep(5)
        print("网络不通\n")
    except ntplib.NTPException:
        sleep(5)
        print("请求NTP时间同步超时\n")
    else:
        return ctime(response.tx_time)


# 探测包信息类,包括发送的时间,发送的字符串信息
class Send_info(object):
    def __init__(self, packet_number, SendTime, packet_buf):
        self.__packet_number = packet_number
        self.__SendTime = SendTime
        self.__packet_buf = packet_buf

    def __str__(self):
        self.send_str = 'Number ' + str(self.__packet_number) + '  ' + str(self.__SendTime) + '  ' + str(self.__packet_buf)
        return self.send_str

    def __len__(self):
        return len(self.send_str)

# 发送参数类,包括发送包的类型,包的大小(UTF-8中,一个英文字符为一个字节),
# 包的间隔模式（同包的数量的解释,有3种模式:均匀间隔发包,泊松发包,高斯发包）
# 包的数量(指的是整个包的数量,比如共有2个背靠背包,指两个目的结点各收到两个包),
# generate_interval()函数,用来生成发包间隔
class Para_info(object):
    def __init__(self, packet_type, interval_mode, packet_size, nPacket=1):
        self.packet_type = packet_type
        self.interval_mode = interval_mode
        self.packet_size = packet_size
        self.nPacket = nPacket

    def generate_interval(self, uniform_interval=2, poisson_lambda=3, norm_mean=5, norm_standarddeviation=1):
        interval = -1
        while interval < 0:        # 高斯分布可能随机到负数
            if self.interval_mode == UNIFORM:      # 均匀发包
                interval = uniform_interval
            elif self.interval_mode == POISSON:    # 泊松发包
                interval = stats.poisson.rvs(poisson_lambda)
            elif self.interval_mode == GAUSS:      # 高斯发包(正态分布)
                interval = stats.norm.rvs(norm_mean, norm_standarddeviation)
            else:
                raise ValueError("Interval Mode '%s' Not Found" % self.interval_mode)
        return interval

"""
该类用来执行客户端的发送命令,是一个基类.
可用于发送单播,背靠背包或三明治包
"""
class UDPSend(object):
    def Sendpacket(self, sock, ListAddress, para_infomation):
        pass

    # 确定包的内容,参数为小包的字节数,三明治包中大包的大小在发送函数中进行控制
    def generate_packet(self, littepacket, packet_number):
        seed = ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
                'e', 'd', 'c', 'b', 'a']
        packet_buf = []
        while len(packet_buf) < littepacket:
            packet_buf.append(random.choice(seed))
        packet_buf = string.join(packet_buf).replace(' ', '')
        Packet = Send_info(packet_number, datetime.now(), packet_buf)
        return Packet

"""
单播包发送类,继承发送基类
(version 3.0---从文件读入多个ip地址,多进程发送单播包)
"""
class SendUnicast(UDPSend):
    def SendTo(self, sock, para_infomation, (addr, port)):
        packet_count = 1     # 包计数器
        while True:
            try:
                # 探测包直接生成,包的信息包括时间及随机产生的字符串
                sock.sendto(str(self.generate_packet(para_infomation.packet_size, packet_count)), (addr, port))
                print "Success to Send Num %s Unicast packet to %s!" % (packet_count, addr)
            except socket.error, e:
                print "Error Send Num %s Unicast Packet: %s" % (packet_count, str(e))
            except Exception, e:
                print "Other Exception When sending Num %s Unicast Packet: %s" % (packet_count, str(e))
            packet_count += 1
            if packet_count > para_infomation.nPacket:
                break         # 当包计数器超过预先设定的发包数时,退出循环
            sleep(para_infomation.generate_interval())    # 发包间隔,每发完一个包,程序等待一段时间

    def Sendpacket(self, sock, ListAddress, para_infomation):
        if para_infomation.packet_type != TYPE_UNICAST:
            raise ValueError("Wrong Packet Type: %s" % para_infomation.packet_type)
        # 多线程发送不同目的地址的单播包
        thread_pool = list()
        try:
            for i in xrange(len(ListAddress)):
                thread_pool.append(threading.Thread(target=self.SendTo, args=(sock, para_infomation, ListAddress[i])))
        except BaseException, e:
            print "Error Creating Thread: %s" % e
        else:
            try:
                for thread in thread_pool:
                    thread.start()
            except BaseException, e:
                print "Error Start Thread (%s): %s" % (threading.current_thread().name, e)
            else:
                for thread in thread_pool:
                    thread.join()

        print "Closing Connection to the Server..."
        sock.close()

"""
背靠背包发送类,继承发送基类
(Version 3.0---多进程发包,创建两个子进程,分别用来发第一个包与第二个包)
"""
class SendBackToBack(UDPSend):
    # 对Socket的sendto函数进行重写,以实现多线程的发送多探测包
    def SendTo(self, sock, para_infomation, (addr, port)):
        packet_count = 1
        while True:
            try:
                sock.sendto(str(self.generate_packet(para_infomation.packet_size, packet_count)), (addr, port))
                print "Success to Send Num %s BTB Packet to %s" % (packet_count, addr)
            except socket.error, e:
                print "Error Send Num %s BTB Packet to %s: %s" % (packet_count, addr, str(e))
            except Exception, e:
                print "Other Exception When Sending Num %s BTB Packet: %s" % (packet_count, str(e))
            packet_count += 1
            if packet_count > para_infomation.nPacket:
                break                 # 当包计数器超过预先设定的发包数时,退出循环
            sleep(para_infomation.generate_interval())           # 发包间隔,每发完一个包,程序等待一段时间

    def Sendpacket(self, sock, ListAddress, para_infomation):
        if para_infomation.packet_type != TYPE_BACKTOBACK:
            raise ValueError("Wrong Packet Type: %s" % para_infomation.packet_type)
        packet_count = 1      # 包计数器
        # 子进程1用来发送背靠背包的第一个包
        # 子进程2用来发送背靠背包的第二个包
        child_process1 = Process(target=self.SendTo, args=(sock, para_infomation, ListAddress[0]))
        child_process2 = Process(target=self.SendTo, args=(sock, para_infomation, ListAddress[1]))

        # start函数：启动子进程,进行发包
        child_process1.start()
        print "Process %s is sending packet to %s......" % (child_process1.pid, ListAddress[0][0])
        child_process2.start()
        print "Process %s is sending packet to %s......" % (child_process2.pid, ListAddress[1][0])
        # join函数：父进程阻塞,子进程关闭后,父进程才会继续运行
        child_process1.join()
        child_process2.join()

        print "Closing Connection to the Server..."
        sock.close()

"""
三明治包发送类,继承发送基类
(Version 3.0---多进程发包,创建两个子进程,第一个子进程用来发送第一个和第三个小探测包,第二个子进程用来发送第二个大探测包)
"""
class SendSandwich(UDPSend):
    # 重写sendto函数,用来发送第一个和第三个小探测包
    def SendToLittle(self, sock, para_infomation, (addr, port), event1, event2):
        packet_count = 1
        while True:
            # 发送三明治包中的第一个小探测包
            try:
                sock.sendto(str(self.generate_packet(para_infomation.packet_size, packet_count)), (addr, port))
                # event1 表示第一个小包发送完毕
                event1.set()
                print "Success to Send Num %s first small sandwich packet to %s" % (packet_count, addr)
            except socket.error, e:
                print "Error to Send Num %s first small sandwich packet to %s: %s" % (packet_count, addr, str(e))
            except Exception, e:
                print "Other Exception When Sending Num %s first small sandwich packet: %s" % (packet_count, str(e))

            # event等待另一个进程发送完三明治包中的第二个大探测包
            event2.wait()

            # 发送三明治包中的第三个小探测包
            try:
                sock.sendto(str(generate_packet(para_infomation.packet_size)), (addr, port))
                print "Success to Send Num %s third small sandwich packet to %s" % (packet_count, addr)
            except socket.error, e:
                print "Error to Send Num %s third small sandwich packet to %s: %s" % (packet_count, addr, str(e))
            except Exception, e:
                print "Other Exception When Sending Num %s third small sandwich packet: %s" % (packet_count, str(e))

            # 发送完第三个小包后,将事件event清除,使下次发包时序正确
            event1.clear()
            event2.clear()
            packet_count += 1
            if packet_count > para_infomation.nPacket:
                break                 # 当包计数器超过预先设定的发包数时,退出循环
            sleep(para_infomation.generate_interval())           # 发包间隔,每发完一个包,程序等待一段时间

    # 重写sendto函数,用来发送第二个大探测包
    def SendToLarge(self, sock, para_infomation, (addr, port), event1, event2):
        packet_count = 1
        while True:
            try:
                # 等待第一个小包发送完毕
                event1.wait()
                sock.sendto(str(generate_packet(para_infomation.packet_size)) * 20, (addr, port))
                # 发送完大包后,将时间event设置为已发生,使另外一个子进程继续发送第三个小探测包
                event2.set()
                print "Success to Send Num %s second large sandwich packet to %s" % (packet_count, addr)
            except socket.error, e:
                print "Error to Send Num %s second large sandwich packet to %s: %s" % (packet_count, addr, str(e))
            except Exception, e:
                print "Other Exception When Sending Num %s second large sandwich packet: %s" % (packet_count, str(e))
            packet_count += 1
            if packet_count > para_infomation.nPacket:
                break                 # 当包计数器超过预先设定的发包数时,退出循环
            sleep(para_infomation.generate_interval())           # 发包间隔,每发完一个包,程序等待一段时间

    def Sendpacket(self, sock, ListAddress, para_infomation):
        if para_infomation.packet_type != TYPE_SANDWICH:
            raise ValueError("Wrong Packet Type: %s" % para_infomation.packet_type)
        # 事件event用于两个进程间的同步通信,使发包时序正确
        event1 = Event()
        event2 = Event()

        child_process1 = Process(target=self.SendToLittle, args=(sock, para_infomation, ListAddress[0], event1, event2))
        child_process2 = Process(target=self.SendToLarge, args=(sock, para_infomation, ListAddress[1], event1, event2))
        # 启动进程
        child_process1.start()
        print "Process %s is sending packet to %s......" % (child_process1.pid, ListAddress[0][0])
        child_process2.start()
        print "Process %s is sending packet to %s......" % (child_process2.pid, ListAddress[1][0])

        # 父进程阻塞,等待两个子进程关闭后,父进程继续运行
        child_process1.join()
        child_process2.join()

        print "Closing Connection to the Server..."
        sock.close()