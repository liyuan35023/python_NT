__author__ = 'liyuan35023'
# -*- coding: utf-8 -*-

import os
import SocketServer
from datetime import datetime


SERVER_HOST = 'localhost'
SERVER_PORT = 9999
ECHO_MSG = 'Hello echo server!'
TIMEOUT = 10000

"""
使用SocketServer模块实现了服务器端收包的多线程
First，创建一个请求处理程序，说明如何处理客户端请求。这个请求处理类需要继承自BaseRequestHandler类。
       请求处理类中，必须重写handle()方法，这个方法将说明如何处理客户的请求。
Second，需要实例化（先创建一个新的类，继承自thread或者forking和服务器类中的一个）4个基本服务器类中的其中一个，
       向其中传入服务器地址参数与请求处理类参数。
Then，然后调用服务器对象的handle_request()或者serve_forever()方法来处理一个或者多个请求。
Finally，调用server_close()方法来关闭套接字。
"""


class ForkingServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        print "Process %s Received data:'%s' from %s.   Arrived time: %s" % (os.getpid(), data, self.client_address,
                                                                             datetime.now())
        return


class ForkingServer(SocketServer.ForkingMixIn, SocketServer.UDPServer):
    pass


def main():
    print "Waiting for data..."
    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    print "Server loop running PID: %s" % os.getpid()
    server.serve_forever()

if __name__ == '__main__':
    main()