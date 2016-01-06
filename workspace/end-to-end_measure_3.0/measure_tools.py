__author__ = 'liyuan35023'
# -*- coding: utf-8 -*-

import argparse
import os
import Client_Send
import forkingServer_Receive

SEND_RECV = 0
CLIENTSEND = 1
SERVERRECV = 2

def client_send():
    Client_Send.main()


def server_receive():
    forkingServer_Receive.main()

"""
端到端测量主程序.包括客户发送以及服务器接收.
共有三种模式：
0---同时发送与接收(父进程接收,子进程发送)
1---启动发送模式
2---启动接收模式
"""


def main():
    # 解析从命令行传入的参数,确定测量工具的模式(0--发送模式与接收模式都启动,1--发送,2--接收)
    parse = argparse.ArgumentParser(description="SEND mode or RECV mode")
    parse.add_argument("--mode", action="store", dest="mode", type=int, required=True)
    given_args = parse.parse_args()
    mode = given_args.mode

    if mode == 1:
        client_send()           # 客户端发包模式
    elif mode == 2:
        server_receive()        # 服务器收包模式
    elif mode == 0:
        pid = os.fork()
        if pid == 0:
            client_send()       # 子进程执行发送任务,发送完毕后子进程关闭
        else:
            server_receive()    # 父进程执行接收任务,接收服务器一直运行
    else:
        raise ValueError("mode not found!please check your argparse...")

if __name__ == "__main__":
    main()
