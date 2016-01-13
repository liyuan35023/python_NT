# -*- coding: utf-8 -*-
__author__ = 'liyuan35023'


import os
import os.path
import socket
import random
import string
import ntplib
import threading
import struct
from multiprocessing import Process, Event, Value
from time import *
from datetime import datetime
from scipy import stats
import imp


# 发送包的类型
TYPE_UNICAST = 0
TYPE_BACKTOBACK = 1
TYPE_SANDWICH = 2

# 发送包时间间隔模式
UNIFORM = 0
POISSON = 1
GAUSS = 2


def get_time():
    """
    时间显示函数,用来返回网络时间
    """
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


class Send_info(object):
    """
    探测包信息类,包括包的序号,发送的时间,发送的字符串信息,发送的总包数
    """
    def __init__(self, packet_number, SendTime, total_packet, packet_buf):
        self.__packet_number = packet_number
        self.__SendTime = SendTime
        self.__total_packet = total_packet
        self.__packet_buf = packet_buf

    def __str__(self):
        # self.send_str = 'Number ' + str(self.__packet_number) + '  ' + str(self.__SendTime) + '  ' +
        #                                 str(self.__packet_buf)

        # 打包发送信息
        imp.acquire_lock()    # 防止发生_strptime_time错误
        timearray = strptime(str(self.__SendTime), "%Y-%m-%d %H:%M:%S.%f")
        imp.release_lock()
        timestamp = int(mktime(timearray))
        length = len(str(self.__packet_buf))
        self.send_str = struct.pack('>6s3I%ss' % length, 'Number', self.__packet_number, timestamp,
                                    self.__total_packet, self.__packet_buf)
        return self.send_str

    def __len__(self):
        return len(self.send_str)

    def get_SendTime(self):
        return self.__SendTime


class Para_info(object):
    """
    发送参数类,包括发送包的类型,包的大小(UTF-8中,一个英文字符为一个字节),
    包的间隔模式（同包的数量的解释,有3种模式:均匀间隔发包,泊松发包,高斯发包）
    包的数量(指的是整个包的数量,比如共有2个背靠背包,指两个目的结点各收到两个包),
    generate_interval()函数,用来生成发包间隔
    """
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


class UDPSend(object):
    """
    该类用来执行客户端的发送命令,是一个基类.
    可用于发送单播,背靠背包或三明治包
    """
    def Sendpacket(self, sock, ListAddress, para_infomation):
        pass

    # 确定包的内容,参数为小包的字节数,三明治包中大包的大小在发送函数中进行控制
    @staticmethod
    def generate_packet(littepacket, packet_number, total_packet):
        seed = ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
                'e', 'd', 'c', 'b', 'a']
        packet_buf = []
        while len(packet_buf) < littepacket:
            packet_buf.append(random.choice(seed))
        packet_buf = string.join(packet_buf).replace(' ', '')
        Packet = Send_info(packet_number, datetime.now(), total_packet, packet_buf)
        return Packet

    # 计算发包速率
    @staticmethod
    def calculate_sendrate(time, bytes):
        rate = bytes / float(time)
        return rate

    # FIXME: 需不需要在发送端将发送特征写入文件？
    # 发送完成后,向文件中写入发送的特征
    @staticmethod
    def write_feature(addr, packettype, intervalmode, numberOfpacket, rate):
        dict1 = {0: 'Unicast', 1: 'BackToBack', 2: 'Sandwich'}
        dict2 = {0: 'Uniform', 1: 'Poisson', 2: 'Gauss'}
        if not os.path.isdir('writefiles'):
            os.mkdir('./writefiles')
        try:
            file0 = open('./writefiles/sentfeature-%s' % addr, 'w')   # 生成多个文件
        except IOError, e:
            print "Can't create 'sentfeature' file:%s" % e
        else:
            if isinstance(addr, str):
                file0.write('目的地址：%s\n' % addr)
            elif isinstance(addr, list):
                file0.write('目的地址：%s, %s\n' % (addr[0], addr[1]))
            file0.write('发包类型：%s\n' % dict1[packettype])
            file0.write('发包间隔采样方式：%s\n' % dict2[intervalmode])
            file0.write('发包数目：%s\n' % numberOfpacket)
            file0.write('发包速率：%s Bytes/s\n' % rate)
        finally:
            file0.close()


class SendUnicast(UDPSend):
    """
    单播包发送类,继承发送基类
    (version 3.0---从文件读入多个ip地址,多进程发送单播包)
    """
    def SendTo(self, sock, para_information, (addr, port)):
        packet_count = 1     # 包计数器
        while True:
            try:
                # 探测包直接生成,包的信息包括时间及随机产生的字符串及包的序号
                packet = self.generate_packet(para_information.packet_size, packet_count, para_information.nPacket)
                sock.sendto(str(packet), (addr, port))
                print "Success to Send Num %s Unicast packet to %s!" % (packet_count, addr)
            except socket.error, e:
                print "Error Send Num %s Unicast Packet to %s: %s" % (packet_count, addr, str(e))
            except Exception, e:
                print "Other Exception When sending Num %s Unicast Packet: %s" % (packet_count, str(e))
            else:
                # 计算报文发送速率,单位为bytes/s.并在发送完成后,将发送特征写入文件
                if packet_count == 1:
                    start_time = packet.get_SendTime()
                elif packet_count == para_information.nPacket:
                    end_time = packet.get_SendTime()

                    # 如果在一秒内发完所有包则需要用微秒计算
                    if (end_time - start_time).seconds > 0:
                        transmissiontime = (end_time - start_time).seconds
                    else:
                        transmissiontime = (end_time - start_time).microseconds / float(1000000)
                    # len(packet)实际发的字节数,utf-8中英文与数字都只占一个字节,所以不用转换为bytes类型
                    sum_bytes = packet_count * (len(packet) - 1)
                    Transmission_rate = self.calculate_sendrate(transmissiontime, sum_bytes)
                    print "Send to %s ,Transmission rate is %s" % (addr, Transmission_rate)
                    # 将发送特征写入文件
                    # self.write_feature(addr, para_information.packet_type, para_information.interval_mode,
                    #                    para_information.nPacket, Transmission_rate)

            packet_count += 1
            if packet_count > para_information.nPacket:
                break         # 当包计数器超过预先设定的发包数时,退出循环
            sleep(para_information.generate_interval())    # 发包间隔,每发完一个包,程序等待一段时间

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


class SendBackToBack(UDPSend):
    """
    背靠背包发送类,继承发送基类
    (Version 3.0---多进程发包,创建两个子进程,分别用来发第一个包与第二个包)
    """

    # 对Socket的sendto函数进行重写,以实现多线程的发送多探测包
    def SendTo(self, sock, para_information, (addr, port), sum_bytes, transmission_time):
        packet_count = 1

        while True:
            try:
                # 探测包直接生成,包的信息包括时间及随机产生的字符串及包的序号
                packet = self.generate_packet(para_information.packet_size, packet_count)
                sock.sendto(str(packet), (addr, port))
                print "Success to Send Num %s BTB Packet to %s" % (packet_count, addr)
            except socket.error, e:
                print "Error Send Num %s BTB Packet to %s: %s" % (packet_count, addr, str(e))
            except Exception, e:
                print "Other Exception When Sending Num %s BTB Packet to %s: %s" % (packet_count, addr, str(e))
            else:
                if packet_count == 1:
                    start_time = packet.get_SendTime()
                elif packet_count == para_information.nPacket:
                    end_time = packet.get_SendTime()
                    # len(packet)实际发的字节数,utf-8中英文与数字都只占一个字节,所以不用转换为bytes类型
                    sum_bytes.value = packet_count * (len(packet) - 1)
                    # 如果在一秒内发完所有包则需要用微秒计算
                    if (end_time - start_time).seconds > 0:
                        transmission_time.value = (end_time - start_time).seconds
                    else:
                        transmission_time.value = (end_time - start_time).microseconds / float(1000000)
            packet_count += 1
            if packet_count > para_information.nPacket:
                break                 # 当包计数器超过预先设定的发包数时,退出循环
            sleep(para_information.generate_interval())           # 发包间隔,每发完一个包,程序等待一段时间


    def Sendpacket(self, sock, ListAddress, para_information):
        if para_information.packet_type != TYPE_BACKTOBACK:
            raise ValueError("Wrong Packet Type: %s" % para_information.packet_type)
        # 分别向两个进程传入Value类型的参数,可以改变value的值并返回
        sum_bytes1 = Value('i', 0)
        sum_bytes2 = Value('i', 0)
        transmission_time1 = Value('i', 0)
        transmission_time2 = Value('i', 0)

        # 子进程1用来发送背靠背包的第一个包
        # 子进程2用来发送背靠背包的第二个包
        child_process1 = Process(target=self.SendTo, args=(sock, para_information, ListAddress[0],
                                                           sum_bytes1, transmission_time1))
        child_process2 = Process(target=self.SendTo, args=(sock, para_information, ListAddress[1],
                                                           sum_bytes2, transmission_time2))

        # start函数：启动子进程,进行发包
        child_process1.start()
        print "Process %s is sending packet to %s......" % (child_process1.pid, ListAddress[0][0])
        child_process2.start()
        print "Process %s is sending packet to %s......" % (child_process2.pid, ListAddress[1][0])
        # join函数：父进程阻塞,子进程关闭后,父进程才会继续运行
        child_process1.join()
        child_process2.join()

        # 计算发包速率
        sum_bytes = sum_bytes1.value + sum_bytes2.value
        if transmission_time1.value == transmission_time1.value:
            print transmission_time1.value
            Transmission_rate = self.calculate_sendrate(transmission_time1.value, sum_bytes)
            print "Transmission rate is %s" % Transmission_rate
            # self.write_feature(ListAddress, para_information.packet_type, para_information.interval_mode,
            #                    para_information.nPacket, Transmission_rate)
        else:
            raise ValueError("transmissiontime1 not equal to transmission2!")
        print "Closing Connection to the Server..."
        sock.close()


class SendSandwich(UDPSend):
    """
    三明治包发送类,继承发送基类
    (Version 3.0---多进程发包,创建两个子进程,第一个子进程用来发送第一个和第三个小探测包,第二个子进程用来发送第二个大探测包)
    """

    # 重写sendto函数,用来发送第一个和第三个小探测包
    def SendToLittle(self, sock, para_information, (addr, port), event1, event2, sum_bytes, transmission_time):
        packet_count = 1
        while True:
            # 发送三明治包中的第一个小探测包
            try:
                packet = self.generate_packet(para_information.packet_size, packet_count)
                sock.sendto(str(packet), (addr, port))
                # event1 表示第一个小包发送完毕
                event1.set()
                print "Success to Send Num %s first small sandwich packet to %s" % (packet_count, addr)
            except socket.error, e:
                print "Error to Send Num %s first small sandwich packet to %s: %s" % (packet_count, addr, str(e))
            except Exception, e:
                print "Other Exception When Sending Num %s first small sandwich packet: %s" % (packet_count, str(e))
            else:
                if packet_count == 1:
                    start_time = packet.get_SendTime()
            # event2等待另一个进程发送完三明治包中的第二个大探测包
            event2.wait(1)

            # 发送三明治包中的第三个小探测包
            try:
                packet = self.generate_packet(para_information.packet_size, packet_count)
                sock.sendto(str(packet), (addr, port))
                print "Success to Send Num %s third small sandwich packet to %s" % (packet_count, addr)
            except socket.error, e:
                print "Error to Send Num %s third small sandwich packet to %s: %s" % (packet_count, addr, str(e))
            except Exception, e:
                print "Other Exception When Sending Num %s third small sandwich packet: %s" % (packet_count, str(e))
            else:
                if packet_count == para_information.nPacket:
                    end_time = packet.get_SendTime()
                    # len(packet)实际发的字节数,utf-8中英文与数字都只占一个字节,所以不用转换为bytes类型
                    sum_bytes.value = packet_count * (len(packet) - 1) * 2
                    # 如果在一秒内发完所有包则需要用微秒计算
                    if (end_time - start_time).seconds > 0:
                        transmission_time.value = (end_time - start_time).seconds
                    else:
                        transmission_time.value = (end_time - start_time).microseconds / float(1000000)
            # 发送完第三个小包后,将事件event清除,使下次发包时序正确
            event1.clear()
            event2.clear()
            packet_count += 1
            if packet_count > para_information.nPacket:
                break                 # 当包计数器超过预先设定的发包数时,退出循环
            sleep(para_information.generate_interval())           # 发包间隔,每发完一个包,程序等待一段时间

    # 重写sendto函数,用来发送第二个大探测包
    def SendToLarge(self, sock, para_information, (addr, port), event1, event2, sum_bytes, transmission_time):
        packet_count = 1
        while True:
            try:
                # 等待第一个小包发送完毕
                event1.wait(1)
                packet = self.generate_packet(para_information.packet_size, packet_count)
                sock.sendto(str(packet) * 25, (addr, port))
                # 发送完大包后,将时间event设置为已发生,使另外一个子进程继续发送第三个小探测包
                event2.set()
                print "Success to Send Num %s second large sandwich packet to %s" % (packet_count, addr)
            except socket.error, e:
                print "Error to Send Num %s second large sandwich packet to %s: %s" % (packet_count, addr, str(e))
            except Exception, e:
                print "Other Exception When Sending Num %s second large sandwich packet: %s" % (packet_count, str(e))
            else:
                if packet_count == 1:
                    start_time = packet.get_SendTime()
                elif packet_count == para_information.nPacket:
                    end_time = packet.get_SendTime()
                    # len(packet)实际发的字节数,utf-8中英文与数字都只占一个字节,所以不用转换为bytes类型
                    sum_bytes.value = packet_count * (len(packet) - 1) * 20
                    # 如果在一秒内发完所有包则需要用微秒计算
                    if (end_time - start_time).seconds > 0:
                        transmission_time.value = (end_time - start_time).seconds
                    else:
                        transmission_time.value = (end_time - start_time).microseconds / float(1000000)

            packet_count += 1
            if packet_count > para_information.nPacket:
                break                 # 当包计数器超过预先设定的发包数时,退出循环
            sleep(para_information.generate_interval())           # 发包间隔,每发完一个包,程序等待一段时间

    def Sendpacket(self, sock, ListAddress, para_information):
        if para_information.packet_type != TYPE_SANDWICH:
            raise ValueError("Wrong Packet Type: %s" % para_information.packet_type)
        sum_bytes1 = Value('i', 0)
        sum_bytes2 = Value('i', 0)
        transmission_time1 = Value('i', 0)
        transmission_time2 = Value('i', 0)

        # 事件event用于两个进程间的同步通信,使发包时序正确
        event1 = Event()
        event2 = Event()

        child_process1 = Process(target=self.SendToLittle, args=(sock, para_information, ListAddress[0],
                                                                 event1, event2, sum_bytes1, transmission_time1))
        child_process2 = Process(target=self.SendToLarge, args=(sock, para_information, ListAddress[1],
                                                                event1, event2, sum_bytes2, transmission_time2))
        # 启动进程
        child_process1.start()
        print "Process %s is sending packet to %s......" % (child_process1.pid, ListAddress[0][0])
        child_process2.start()
        print "Process %s is sending packet to %s......" % (child_process2.pid, ListAddress[1][0])

        # 父进程阻塞,等待两个子进程关闭后,父进程继续运行
        child_process1.join()
        child_process2.join()

        # 计算发包速率
        sum_bytes = sum_bytes1.value + sum_bytes2.value
        if transmission_time1.value == transmission_time1.value:
            Transmission_rate = self.calculate_sendrate(transmission_time1.value, sum_bytes)
            print "Transmission rate is %s" % Transmission_rate
            # self.write_feature(ListAddress, para_information.packet_type, para_information.interval_mode,
            #                    para_information.nPacket, Transmission_rate)
        else:
            raise ValueError("transmissiontime1 not equal to transmission2!")

        print "Closing Connection to the Server..."
        sock.close()
