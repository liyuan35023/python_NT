__author__ = 'liyuan35023'

# !/home/mimiasd/PycharmProjects/workspace python27


import ntplib
from time import ctime

def print_time():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('cn.ntp.org.cn')
    print ctime(response.tx_time)

if __name__ == "__main__":
    print_time()
