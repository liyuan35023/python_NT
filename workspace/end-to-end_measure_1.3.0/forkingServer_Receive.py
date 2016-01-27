# -*- coding: utf-8 -*-
__author__ = 'liyuan35023'


import os
import os.path
import socket
import SocketServer
from datetime import datetime


SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999

"""  多进程！
使用SocketServer模块实现了服务器端收包的多进程
First，创建一个请求处理程序，说明如何处理客户端请求。这个请求处理类需要继承自BaseRequestHandler类。
       请求处理类中，必须重写handle()方法，这个方法将说明如何处理客户的请求。
Second，需要实例化（先创建一个新的类，继承自thread或者forking和服务器类中的一个）4个基本服务器类中的其中一个，
       向其中传入服务器地址参数与请求处理类参数。
Then，然后调用服务器对象的handle_request()或者serve_forever()方法来处理一个或者多个请求。
Finally，调用server_close()方法来关闭套接字。
"""


class ForkingServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()    # request[0]为收到的信息.request[1]为它的类型.strip--去掉换行符
        now = datetime.now()              # 收到包的时间
        print "Process %s Received data:'%s' from %s.  Arrived time: %s" % (os.getpid(), data, self.client_address,
                                                                            now)
        if not os.path.isdir('writefiles'):
            os.mkdir('./writefiles')
        try:
            file1 = open('./writefiles/recvfeature-%s' % self.client_address[0], 'a')   # 生成多个文件
        except IOError, e:
            print "Can't create or open 'recveature' file:" % e
        else:
            file1.write("data:'%s' from %s. Arrived time: %s\n" % (data, self.client_address, now))
        # finally:
        #     file1.close()
        return


class ForkingServer(SocketServer.ForkingMixIn, SocketServer.UDPServer):
    # 重写bind函数,设置套接字选项,使地址可以重用
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()


def main():
    print "Waiting for data..."

    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    print "Server loop running PID: %s" % os.getpid()
    server.serve_forever()

if __name__ == "__main__":
    main()
