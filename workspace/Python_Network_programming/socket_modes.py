__author__ = 'liyuan35023'

#!/home/mimiasd/PycharmProjects/workspace python27


import socket

def test_socket_modes():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(0)
    s.settimeout(0.5)
    s.bind(("127.0.0.1", 13555))
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    socket_address = s.getsockname()
    print "Trivial Server launched on socket: %s" % str(socket_address)
    #print socket_address
    while(1):
        s.listen(1)


if __name__ == "__main__":
    test_socket_modes()