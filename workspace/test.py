__author__ = 'liyuan35023'
 # -*- coding: utf-8 -*-
import string
# # import datetime
# # import time
import math
import random

def poisson(L):
    """
    poisson distribution
    return a integer random number, L is the mean value
    """
    p = 1.0
    k = 0
    e = math.exp(-L)
    while p >= e:
        u = random.random()  #generate a random floating point number in the range [0.0, 1.0)
        p *= u
        k += 1
    return k-1

print poisson(5)



from scipy import stats

poi = stats.poisson.pmf(4, 5)
print poi

rvss = stats.poisson.rvs(5, size = 5)
print rvss
print rvss[0]

normm = stats.norm.rvs()
print normm



def abd(a, b=4, c=None):
    return c
a = abd(None,c=3)
print a


# class send_info(object):
#     def __init__(self, SendTime, packet_buf):
#         self.__SendTime = SendTime
#         self.__packet_buf = packet_buf
#     def __str__(self):
#         send_str = str(self.__SendTime) + str(self.__packet_buf)
#         return send_str
#     def __len__(self):
#         return len(str(self.__SendTime) + str(self.__packet_buf))
#     def print_str(self):
#         print str(self.__SendTime) + str(self.__packet_buf)
#
#
# if __name__ == "__main__":
#     s = send_info("3344", "liyuan")
#     print s
#     print len(s)
#
# # def abc(a, b, c):
# #      return a*10000 + b*100 + c
# #
# # list1 = [11, 22, 33]
# # list2 = [44, 55, 66]
# # list3 = [77,88,99]
# # list4 = [1,2,3]
# # print(map(abc,list1,list2, list3))
# #
# # d = {1:abc, 2:44, 3:445}
# # print d[3]
# # print d.get(1)(1,2,3)
#
# L = [(1,2),(3,5),(4,2)]
# print L[0][1]
# a = 1
# strrr = 'fdasf'
# print strrr * 3
# print a
#
print random.randint(1,50)
print random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()')
print random.sample('abcdefghijklmnopqrstuvwxyz!@#$%^&*()', 5)
print string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 5)).replace(' ', '')

#
# print datetime.datetime.now()
# print datetime.datetime.now().microsecond
# print time.localtime()