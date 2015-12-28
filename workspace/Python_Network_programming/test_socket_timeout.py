__author__ = 'liyuan35023'

# ! /home/mimiasd/PycharmProjects/workspace python27

import socket


def test_socket_timeout():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print "Default timeout: %s" % s.gettimeout()
    s.settimeout(100)
    print "Current tiemout: %s" % s.gettimeout()

if __name__ == "__main__":
    test_socket_timeout()