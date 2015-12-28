__author__ = 'liyuan35023'

# !/home/mimiasd/PycharmProjects/workspace python27
import socket
import logging

def get_remote_machine_info():
    remote_host = 'lyl-H81M-DS2'
    try:
        #print "IP address :%s" %socket.gethostbyname(remote_host)
        print_IP(remote_host)
    except BaseException, err_msg:
        print "%s: %s" % (remote_host, err_msg)
        logging.exception(err_msg)

def print_IP(host_name):
    print "IP address :%s" % socket.gethostbyname(host_name)

if __name__ == '__main__':
    get_remote_machine_info()
