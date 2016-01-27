# -*- coding: utf-8 -*-
__author__ = 'liyuan35023'

import os
import os.path
import matplotlib.pyplot as plt
import numpy


def scan_files(directory, prefix=None, postfix=None):
    files_list=[]
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root, special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root, special_file))
                else:
                    files_list.append(os.path.join(root, special_file))
    return files_list


if __name__ == '__main__':
    files_list = scan_files('/home/mimiasd/twohours_data/', 'packet_')

    for files in files_list:
        datafile = open(files, 'r')

        line_number = 0
        delay_list = list()
        while True:
            a = datafile.readline().split('  ')
            if a != ['']:
                if int(a[2][3:4]) != int(a[1][3:4]):
                    delay = float(a[2][6:14]) + 60 - float(a[1][6:14])
                else:
                    delay = float(a[2][6:14]) - float(a[1][6:14])
                delay_list.append(delay)
                line_number += 1
            else:
                break
        datafile.close()
        # print delay_list
        delay_array = numpy.array(delay_list)
        delay_mean = delay_array.mean()
        if delay_mean > 10:
            continue
        # print delay_mean
        delay_variance = delay_array.var()
        if delay_variance > 100:
            continue
        # print delay_variance
        # print line_number
        loss_rate = 1-(line_number/float(72000))
        if loss_rate < 0:
            continue
        # print loss_rate

        plt.figure(1, figsize=(10, 5))
        plt.plot(loss_rate, delay_mean, "-o", label=u"delay_mean", color="red")
        plt.xlabel('loss rate')
        plt.ylabel('delay mean')

        plt.figure(2, figsize=(10, 5))
        plt.plot(loss_rate, delay_variance, "-o", label=u"delay_variance", color="red")
        plt.xlabel('loss rate')
        plt.ylabel('delay variance')

    plt.show()

