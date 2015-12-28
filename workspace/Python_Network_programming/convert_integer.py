__author__ = 'liyuan35023'

#!/home/mimiasd/PycharmProjects/workspace python27

import socket


def convert_integer():
    data = 1234
    # 32bits
    print "original: %s => Long host: %s, Long network: %s"\
        % (data, socket.ntohl(data), socket.htonl(data))
    # 16bits
    print "original: %s => Short host: %s, Short network: %s"\
        % (data, socket.ntohs(data), socket.htons(data))

if __name__ == "__main__":
    convert_integer()
