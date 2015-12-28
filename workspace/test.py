__author__ = 'liyuan35023'
# -*- coding: utf-8 -*-

class send_info(object):
    def __init__(self, SendTime, packet_buf):
        self.__SendTime = SendTime
        self.__packet_buf = packet_buf
    def __str__(self):
        send_str = str(self.__SendTime) + str(self.__packet_buf)
        return send_str
    def __len__(self):
        return len(str(self.__SendTime) + str(self.__packet_buf))
    def print_str(self):
        print str(self.__SendTime) + str(self.__packet_buf)


if __name__ == "__main__":
    s = send_info("3344", "liyuan")
    print s
    print len(s)

# def abc(a, b, c):
#      return a*10000 + b*100 + c
#
# list1 = [11, 22, 33]
# list2 = [44, 55, 66]
# list3 = [77,88,99]
# list4 = [1,2,3]
# print(map(abc,list1,list2, list3))
#
# d = {1:abc, 2:44, 3:445}
# print d[3]
# print d.get(1)(1,2,3)

L = [(1,2),(3,5),(4,2)]
print L[0][1]
