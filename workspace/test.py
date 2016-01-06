__author__ = 'liyuan35023'
# from datetime import datetime, time
# from time import sleep
# a = datetime.now()
# print a
# sleep(2)
# c = datetime.now()
# print c
# print (c-a).seconds / 3.0
strr = 'fadfas'
print strr.encode('ascii')




# import urllib2
# import cookielib
# url = 'http://www.baidu.com'
#
# print 'fang fa 1:'
# response1 = urllib2.urlopen(url)
#
# print response1.getcode()
# print len(response1.read())
#
# request = urllib2.Request(url)
# request.add_header('user-agent', 'Mozilla/5.0')
# response2 = urllib2.urlopen(request)
# print 'fang fa 2:'
#
# print response2.getcode()
# print len(response2.read())
#
#
#
# print 'fang fa 3'
#
# cj = cookielib.CookieJar()
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# urllib2.install_opener(opener)
# response3 = urllib2.urlopen(url)
#
#
# print response3.getcode()
# print response3.read()
# ListAddress = []
# with open('./end-to-end_measure_3.0/readfiles/Unicast_ip', 'r') as f_Unicast:
#             for line in f_Unicast.readlines():
#                 #if line.strip():
#                 ListAddress.append(line.strip())
# # while '' in ListAddress:
# #     ListAddress.remove('')
# print ListAddress
#  # -*- coding: utf-8 -*-
import string
# # import datetime
# # import time
# import math
# import random
#
# def poisson(L):
#     """
#     poisson distribution
#     return a integer random number, L is the mean value
#     """
#     p = 1.0
#     k = 0
#     e = math.exp(-L)
#     while p >= e:
#         u = random.random()  #generate a random floating point number in the range [0.0, 1.0)
#         p *= u
#         k += 1
#     return k-1
#
# print poisson(5)
#
#
#
# from scipy import stats
#
# poi = stats.poisson.pmf(4, 5)
# print poi
#
# rvss = stats.poisson.rvs(5, size = 5)
# print rvss
# print rvss[0]
#
# normm = stats.norm.rvs()
# print normm
#
#
#
# def abd(a, b=4, c=None):
#     return c
# a = abd(None, c=3)
# print a,


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
# print random.randint(1,50)
# print random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()')
# print random.sample('abcdefghijklmnopqrstuvwxyz!@#$%^&*()', 5)
# print string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 5)).replace(' ', '')

#
# print datetime.datetime.now()
# print datetime.datetime.now().microsecond
# print time.localtime()

# #coding: utf-8
# import multiprocessing
# import time
#
#
# class test(object):
#
#     def func(msg):
#         print "msg:", msg
#         time.sleep(3)
#         print "end"
#
#     def pooool(self):
#         pool = multiprocessing.Pool(processes=3)
#         for i in xrange(4):
#             msg = "hello %d" %(i)

#
#         print "Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~"
#         pool.close()
#         pool.join()
#         print "Sub-process(es) done."
#
#
#
# #!/usr/bin/env python
# #coding=gbk
#
# import threading
# import time, random,  sys
#
# class Counter:
#     def __init__(self):
#         self.lock = threading.Lock()
#         self.value = 0
#
#     def increment(self):
#         self.lock.acquire()
#         self.value = value = self.value + 1
#         self.lock.release()
#         return value
#
# counter = Counter()
# cond = threading.Condition()
#
# class Worker(threading.Thread):
#
#     def run(self):
#         print self.getName(),  "-- created."
#         cond.acquire()
#         #for i in range(10):
#             # pretend we're doing something that takes 10?00 ms
#             #value = counter.increment()
#             # time.sleep(random.randint(10, 100) / 1000.0)
#         cond.wait()
#         #print self.getName(), "-- task", "finished"
#         cond.release()
#
#
#
# if __name__ == '__main__':
#
#         try:
#             for i in range(3500):
#                 Worker().start() # start a worker
#         except BaseException,  e:

#             time.sleep(5)
#             print "maxium i=",  i
#         finally:
#             cond.acquire()
#             cond.notifyAll()
#             cond.release()
#             time.sleep(3)
#             print threading.currentThread().getName(),  " quit"




# ListAddress = []
# with open('./end-to-end_measure_3.0/readfiles/BackToBack_ip', 'r') as f_BackToBack:
#             for line in f_BackToBack.readlines():
#                 ListAddress.append((line.strip(), 9999))
#                 #ListAddress.reverse()
# print ListAddress