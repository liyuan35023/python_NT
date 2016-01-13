#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liyuan35023'
# import time
from datetime import datetime
# import struct
# a = struct.pack('>I', 65)
# print a
#
# print struct.unpack('>IH', b'\xf0\xf0\xf0\xf0\x80\x80')
q = datetime.now()
# w = datetime.now()
# sr = (w-q).microseconds / float(1000000)
# se = w.microsecond-q.microsecond
# print sr
# print se
# timefsd = str(datetime.now())
# print datetime.now()
# # t = time.time()
# # print t
# # print datetime.fromtimestamp(t)
#
# timearray = time.strptime(timefsd, "%Y-%m-%d %H:%M:%S.%f")
#
# stamp = int(time.mktime(timearray))
# print stamp
# print datetime.fromtimestamp(stamp)
#
# print struct.pack('>I', stamp)
# # print struct.unpack('>10I', struct.pack('>I', stamp))
#
# s = 'fadsfafsd'
# leng =len(s)
# print struct.pack('>I%ss' % leng, 10, s)


import Queue
import threading
import time
import os
queue = Queue.Queue()
queue.put((2, 3))
a= queue.get()

print a
source_ip = '192.168.1.13'
if not os.path.isdir('received_packet'):
            os.mkdir('./received_packet')
try:
    file0 = open('./received_packet/packet_%s' % source_ip, 'a')   # 每个源目的结点对应一个文件
except IOError, e:
    print "Can't create 'packet_%s' file:%s:" % (source_ip, e)
else:
    a = (3, 3, 4)
    file0.write(str(a))
    file0.write(str(q))
finally:
    file0.close()

#
# #
# class ThreadNum(threading.Thread):
#  """没打印一个数字等待1秒，并发打印10个数字需要多少秒？"""
#   def __init__(self, queue):
#     threading.Thread.__init__(self)
#     self.queue = queue
#
#   def run(self):
#     while True:
#       #消费者端，从队列中获取num
#       num = self.queue.get()
#       print "i'm num %s"%(num)
#       time.sleep(1)
#       #在完成这项工作之后，使用 queue.task_done() 函数向任务已经完成的队列发送一个信号
#       self.queue.task_done()
#
# start = time.time()
# def main():
#   #产生一个 threads pool, 并把消息传递给thread函数进行处理，这里开启10个并发
#   for i in range(10):
#     t = ThreadNum(queue)
#     t.setDaemon(True)
#     t.start()
#
#   #往队列中填错数据
#   for num in range(10):
#       queue.put(num)
#   #wait on the queue until everything has been processed
#   queue.join()
#
# main()
# print "Elapsed Time: %s" % (time.time() - start)






# from datetime import datetime, time
# from time import sleep
# from multiprocessing import Value
# a = datetime.now()
# print a
# sleep(1)
# c = datetime.now()
# print c
# print (c-a).seconds / 3.0
#
# v = Value('t')
# v.value = a
# print v.value



# strr = 'fadfas'
# print strr.encode('ascii')
# f = 1
# def a():
#
#     b()
#
# def b():
#     print f
#
# if __name__ == "__main__":
#     a()

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