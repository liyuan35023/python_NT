__author__= 'liyuan35023'

import os
import test


print ('Process %s start..'%os.getpid())
pid=os.fork()
if pid==0:
    print('i am the child process %s of process %s'%(os.getpid(),os.getppid()))
else:
    print('i %s just created a child process %s'%(os.getpid(),pid))

#
# print('Process (%s) start...' % os.getpid())
# # Only works on Unix/Linux/Mac:
# pid = os.fork()
# if pid == 0:
#     print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
# else:
#     print('I (%s) just created a child process (%s).' % (os.getpid(), pid))

s = test.send_info("fsda", "fdasf")
print s