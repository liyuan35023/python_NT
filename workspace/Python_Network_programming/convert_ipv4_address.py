__author__ = 'liyuan35023'

# !/home/mimiasd/PycharmProjects/workspace python27

import  socket
from binascii import hexlify

ip_addr_list=['127.0.0.1', '192.168.0.1']

def convert_ipv4_address():
    for ip_addr in ip_addr_list:
        packed_ip_addr = socket.inet_aton(ip_addr)
        unpacked_ip_addr = socket.inet_ntoa(packed_ip_addr)
        print 'IP Address: %s => Packed: %s, Unpacked: %s'\
              % (ip_addr, hexlify(packed_ip_addr), unpacked_ip_addr)

if __name__ == '__main__':
    convert_ipv4_address()