# -*- coding: utf-8 -*-
__author__= 'liyuan35023'


# import os
# import os.path
# import test

from scipy import stats

from collections import Counter
import matplotlib.pyplot as plt

_lambda = 5
plt.figure(1, figsize=(10, 4))

interval = stats.poisson.rvs(5, size=5000)
setin = list(set(interval))
# print setin
rate = []
poisson = []
print "啊"
for x in setin:
    rate.append(float(Counter(interval)[x])/5000)
    poisson.append(stats.poisson.pmf(x, _lambda))

plt.plot(setin, rate, "->", lw=2, label=u"fdsfsadf")
plt.plot(setin, poisson, "-o", lw=2, label=u"poisson", color="red")




import numpy as np
plt.figure(2, figsize=(8, 4))
X = stats.norm()
t = np.arange(-5, 5, 0.01)

plt.plot(t, X.pdf(t))

x = stats.norm.rvs(size=50000)
p, t2 = np.histogram(x, bins=100, normed=True)
t2 = (t2[:-1] + t2[1:])/2
plt.plot(t2, p)
plt.show()

# import matplotlib.pyplot as plt
#
# plt.plot([1,2,3],[10, 20, 30], "-o",lw=2)
# plt.xlabel('tiems')
# plt.ylabel('numbers')
# plt.show()

# # -*- coding: utf-8 -*-
# import numpy as np
# from scipy import stats
# import pylab as pl
#
# _lambda = 10
# pl.figure(figsize=(10,4))
# for i, time in enumerate([1000, 50000]):
#     t = np.random.rand(_lambda*time)*time
#     count, time_edges = np.histogram(t, bins=time, range=(0,time))
#     dist, count_edges = np.histogram(count, bins=20, range=(0,20), normed=True)
#     x = count_edges[:-1]
#     poisson = stats.poisson.pmf(x, _lambda)
#     pl.subplot(121+i)
#     pl.plot(x, dist, "-o", lw=2, label=u"jieguo")
#     pl.plot(x, poisson, "->", lw=2, label=u"poisson", color="red")
#     pl.xlabel(u"c")
#     pl.ylabel(u"pro")
#     pl.title(u"time = %d" % time)
#     pl.legend(loc="lower center")
# pl.subplots_adjust(0.1, 0.15, 0.95, 0.90, 0.2, 0.1)
# pl.show()
# #












# print ('Process %s start..'%os.getpid())
# pid=os.fork()
# if pid==0:
#     print('i am the child process %s of process %s'%(os.getpid(),os.getppid()))
# else:
#     print('i %s just created a child process %s'%(os.getpid(),pid))
#
# #
# # print('Process (%s) start...' % os.getpid())
# # # Only works on Unix/Linux/Mac:
# # pid = os.fork()
# # if pid == 0:
# #     print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
# # else:
# #     print('I (%s) just created a child process (%s).' % (os.getpid(), pid))
#
# s = test.send_info("fsda", "fdasf")
# # print s
# def write_feature(addr):
#     if not os.path.isdir('fdas'):
#         os.mkdir('./fdas')
#
#
#     try:
#         file0 = open('./fdas/sentfeature', 'w')
#     except IOError, e:
#         print "Can't create 'sentfeature' file:" % e
#     else:
#         file0.write('ffsaf  %s' % addr)
#         file0.write('fas')
#
#
# if __name__ == '__main__':
#     write_feature('fsd')
