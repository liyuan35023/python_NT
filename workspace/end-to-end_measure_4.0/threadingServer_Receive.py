# -*- coding: utf-8 -*-
__author__ = 'liyuan35023'


import os
import sys
import socket
import threading
import Queue
import struct
from datetime import datetime

SERVER_HOST = 'localhost'
SERVER_PORT = 9999
BUF_SIZE = 1500

"""
服务器收包多线程：
1,线程1：进行监听
2,线程2：将收到的包unpack,解析,即读取包的信息
3,线程3：根据信息(ip?)将读取到的信息写入文件
4,线程4：local center,处理与local center的信令解释,即配置文件读取(未完成)
5,线程5：向local center上传测量数据,采用p2p模式--快(未完成)
"""


class MultiProcessServer(object):
    """
    服务器收包类
    __init__:初始化时传入Server的地址与端口号.并创建套接字和绑定套接字到接口
             传入两个空queue,一个存放收到的数据(待unpack),另一个存放待写入文件的数据(按格式unpacked)
    """
    def __init__(self, address, port, receiving_queue, writing_queue):
        self.server_address = address
        self.server_port = port
        self.receiving_queue = receiving_queue
        self.writing_queue = writing_queue
        self.sock = self.create_socket()
        self.bind_socket()

    @staticmethod
    def create_socket():
        """Create UDP socket, return socket descriptor"""
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error, e:
            print "Error Create Server socket:%s" % e
        else:
            return server_sock

    def bind_socket(self):
        """Bind socket to (ip_address, port) and Set reuse option to the server_address"""
        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error, e:
            print "Error Setting the reuese_address option:%s" % e
        else:
            try:
                self.sock.bind((self.server_address, self.server_port))
            except socket.error, e:
                print "Error Binding socket to the server_address:%s" % e

    def receive_packet(self):
        """Make server in listening status.Store the information in data.
        need to be called to create a new thread!
        """
        while True:
            try:
                data, client_address = self.sock.recvfrom(BUF_SIZE)
                receive_time = datetime.now()
                # print data
            except socket.error, e:
                print "Error receiving the data:%s" % e
            else:
                # 在子进程1中将收到数据写入receiving_queue
                self.receiving_queue.put((data, client_address, receive_time))
                
    def unpacking_packet(self):
        """Unpacking the received packet,include data and client_address.
        Means that get the item of the receiving_queue,parse it and put the
        unpacked information to the writing_queue.
        need to be called to create a new thread!
        """
        while True:
            try:
                data, client_address, receive_time = self.receiving_queue.get()
                self.receiving_queue.task_done()
            except BaseException, e:
                print "Exception:%s" % e
                continue
            else:
                # 计算随机字符串的长度,18=6(字符:Number)+3(unsigned int)*4(1个unsigned int为4bytes)
                randomstr_len = len(data) - 18
                # unpack收到的数据并存入receive_tuple中,receive_tuple的第二项为包序号,第三项为发送时间戳,第四项为发送包的总数
                receive_tuple = struct.unpack('>6s3I%ss' % randomstr_len, data)
                send_time = datetime.fromtimestamp(receive_tuple[2])   # 将时间戳转化为当地时间
                # 定义writing_tuple为存放要写入文件信息的临时tuple
                writing_tuple = (receive_tuple[1], send_time, receive_time, client_address[0],
                                 SERVER_HOST, receive_tuple[3])
                # 将writing_tuple放入待写文件的queue中
                self.writing_queue.put(writing_tuple)

                #

    def writing_file(self):
        """Get the element in the writing_queue.
        And write it into the output file.
        文件格式每行为：sequence_number, send_time, receive_time, source_ip, destination_ip, total_packet
        need to be called to create a new thread!
        """
        while True:
            sequence_number, send_time, receive_time, source_ip, destination_ip, total_packet \
                = self.writing_queue.get()
            self.writing_queue.task_done()
            # 写入文件
            if not os.path.isdir('received_packet'):
                os.mkdir('./received_packet')
            try:
                file0 = open('./received_packet/packet_%s' % source_ip, 'a')   # 每个源目的结点对应一个文件
            except IOError, e:
                print "Can't create 'packet_%s' file:%s:" % (source_ip, e)
            else:
                file0.write(str(sequence_number)+'  ')
                file0.write(str(send_time)+'  ')
                file0.write(str(receive_time)+'  ')
                file0.write(source_ip+'  ')
                file0.write(destination_ip+'  ')
                file0.write(str(total_packet)+'\n')
            finally:
                file0.close()


def main():
    """主函数,实现多线程收包与写入文件"""

    receiving_queue = Queue.Queue()   # 存放收到得到的数据(待unpack),元素为tuple(data, client_address, receive_time)

    writing_queue = Queue.Queue()     # 存放待写入文件的数据(按格式unpacked),元素为tuple(包序,发送时间,接收时间,源地址,目的地址,总包数)

    # 创建多线程接收服务器的实例,在初始化过程中,创建套接字并绑定套接字到服务器地址接口
    sever = MultiProcessServer(SERVER_HOST, SERVER_PORT, receiving_queue, writing_queue)

    # 创建三个线程,分别执行接收,解包,写文件的任务
    listen_thread = threading.Thread(target=sever.receive_packet, name='listening thread')
    unpack_thread = threading.Thread(target=sever.unpacking_packet, name='unpacking thread')
    write_thread = threading.Thread(target=sever.writing_file, name='writing thread')

    # listen_thread.setDaemon(True)
    # unpack_thread.setDaemon(True)
    # write_thread.setDaemon(True)

    # 启动三个线程
    listen_thread.start()
    unpack_thread.start()
    write_thread.start()


    listen_thread.join()
    unpack_thread.join()
    write_thread.join()
    # receiving_queue.join()
    # writing_queue.join()

    # Never Reach
    # FIXME:The program will not stop until the administrator terminate the process!


if __name__ == '__main__':
    main()
