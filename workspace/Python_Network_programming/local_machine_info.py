__author__ = 'liyuan35023'

# !/home/mimiasd/PycharmProjects/workspace python27

import socket

def print_machine_info():
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname("eth0")
    print "Host name : %s"% host_name
    # print "IP address : %s"% ip_address
    print ip_address
if __name__ == '__main__':
   print_machine_info()

