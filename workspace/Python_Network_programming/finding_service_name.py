import socket
__author__ = 'liyuan35023'


# ! /home/mimiasd/PycharmProjects/workspace python27


def find_service_name():
    protocolname = 'tcp'
    for port in [80, 25]:
        print "Port: %s => service name: %s" % (port, socket.getservbyport(port, 'tcp'))
    print "Port: %s => service name: %s" % (2601, socket.getservbyport(2601))

if __name__ == "__main__":
    find_service_name()
