# -*- conding: utf-8 -*-

import sys

class _slice_file(object):
    '''
    逐行读取一个文件，并从每一行读取指定长度内容重新写入一个新文件
    '''
    def readfile(self, in_filename, out_filename):

        infile = open(in_filename, 'r')
        outfile = open(out_filename, 'w')
        lines = infile.readlines()
        count = 1
        for line in lines:
            if count % 2 != 0:
                outfile.write(line[0:8] + '\n')
            else:
                outfile.write(line[9:49] + '\n')
            count += 1
        outfile.close()

if __name__ == '__main__':
    test = _slice_file()
    test.readfile('MD5.txt', 'MD5_new.txt')
