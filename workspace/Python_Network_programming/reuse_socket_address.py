__author__ = 'liyuan35023'

#!/home/mimiasd/PycharmProjects/workspace python27

import socket
import sys

def reuse_socket_address():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Old state
    old_state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    print "Old sock state: %s" % old_state

    # enable
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    new_state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    print "New sock state: %s" % new_state

    local_port = 8283

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('', local_port))
    srv.listen(1)
    print "listening port: %s" % local_port
    while True:
        try:
            connection, addr = srv.accept()
            print "Connected by %s:%s" % (addr[0], addr[1])
        except KeyboardInterrupt, e:
            break
        except socket.error, msg:
            print "%s" % (msg,)


if __name__ == "__main__":
    reuse_socket_address()

