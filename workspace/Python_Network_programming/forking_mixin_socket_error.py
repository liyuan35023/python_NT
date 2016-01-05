__author__ = 'liyuan35023'
# -*- coding: utf-8 -*-

import os
import socket
import threading
import SocketServer

SERVER_HOST = 'localhost'
SERVER_PORT = 0     #让系统或者内核动态选择端口
BUF_SIZE = 1024
ECHO_MSG = 'Hello echo server!'

"""
    a client to test forking server!
"""
class ForkingClient():
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
    def run(self):
        # send data to the server
        current_process_id = os.getpid()
        print "Process %s Sending echo message to the server : '%s'" % (current_process_id, ECHO_MSG)
        sent_data_length = self.sock.send(ECHO_MSG)
        print "Sent: %d characters, so far...." % sent_data_length

        #Display Server's response
        response = self.sock.recv(BUF_SIZE)
        print "PID %s received: %s" % (current_process_id, response)

    def shutdown(self):
        """cleanup the client socket"""
        self.sock.close()

class ForkingServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        current_process_id = os.getpid()
        response = '%s: %s' % (current_process_id, data)
        print "Server Sending response [current_process_id: data] = [%s]" % response
        self.request.send(response)
        return

class ForkingServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    pass

def main():
    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    print "Server loop running PID: %s" % os.getpid()

    # Launch the client(s)
    client1 = ForkingClient(ip, port)
    client1.run()

    client2 = ForkingClient(ip, port)
    client2.run()


    #Clean Them up
    server.shutdown()
    client1.shutdown()
    client2.shutdown()
    server.socket.close()

if __name__ == '__main__':
    main()
