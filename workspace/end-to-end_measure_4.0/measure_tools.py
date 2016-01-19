__author__ = 'liyuan35023'
# -*- coding: utf-8 -*-

import argparse
import os
import Client_Send
import threadingServer_Receive
import signal
from multiprocessing import Process

SEND_RECV = 0
CLIENTSEND = 1
SERVERRECV = 2


def client_send():
    Client_Send.main()


def server_receive():
    threadingServer_Receive.main()

"""
端到端测量主程序.包括客户发送以及服务器接收.
共有三种模式：
0---同时发送与接收(父进程接收,子进程发送)
1---启动发送模式
2---启动接收模式
"""


def main():
    # 解析从命令行传入的参数,确定测量工具的模式(0--发送模式与接收模式都启动,1--发送,2--接收)
    parse = argparse.ArgumentParser(description="SEND mode or RECEIVE mode")
    parse.add_argument("--mode", action="store", dest="mode", type=int, required=True)
    given_args = parse.parse_args()
    mode = given_args.mode

    """在模式0中,处理发送子进程的退出信号,告诉接收父进程它并不关心子进程的状态,发送完毕后,
    系统正常关闭子进程,这样可以避免僵尸进程的产生.
    """
    # signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    if mode == 1:
        client_send()           # 客户端发包模式
    elif mode == 2:
        server_receive()        # 服务器收包模式
    elif mode == 0:
        # pid = os.fork()
        # if pid == 0:
        #     client_send()       # 子进程执行发送任务,发送完毕后子进程关闭
        #     # os._exit(0)
        # else:
        #     server_receive()    # 父进程执行接收任务,接收服务器一直运行
        send_process = Process(target=client_send)
        receive_process = Process(target=server_receive)

        receive_process.start()
        send_process.start()

        receive_process.join()
        send_process.join()
    else:
        raise ValueError("Unexpected mode!please check your argparse...")

if __name__ == "__main__":
    main()
