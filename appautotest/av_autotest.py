# -*- coding: utf-8 -*-

import re
import time
import sys
import encodings
import telnetlib
import os


from configure_all import *


class AV_Sample_AutoTest(object):

    def __init__(self):
        pass

    def _conn_dut(self, host, username, passwd, dia_username, dia_passwd):
        '''
        telnet连接DUT并连接数据库
        '''
        print('telnet to dut:%s' % host)
        host = host.encode('utf-8')
        username = username.encode('utf-8')
        passwd = passwd.encode('utf-8')
        dia_username = dia_username.encode('utf-8')
        dia_passwd = dia_passwd.encode('utf-8')

        tn = telnetlib.Telnet(host, port=23, timeout=10)
        tn.read_until('Username:'.encode('utf-8'))
        tn.write(username + b'\n')
        tn.read_until(b'Password:')
        tn.write(passwd + b'\n')
        tn.read_until(b'>', 10)
        print('telnet successed, continue...')
        tn.write(b'enable' + b'\n')
        tn.read_until(b'host#')
        tn.write(dia_username + b'\n')
        tn.read_until(b'Password:')
        tn.write(dia_passwd + b'\n')
        tn.read_until(b'/ #', 10)
        print('connect to database...')
        tn.write(b'mysql -u root' + b'\n')
        tn.read_until(b'mysql>', 10)
        tn.write(b'use syslog;' + b'\n')
        tn.read_until(b'mysql>', 10)
        print('connect to database successed, continue...')
        return tn

    def get_avfile_http(self):
        print('start to get av simple file...')
        os.system(
            'wget -P avdownload -r -w 1 -np -nd http://172.17.10.73:8000/avsample/ ')

    def dut_del_database(self):
        '''
        清除数据库中已经产生的AV日志
        '''
        tn = self._conn_dut(dut_host_av, dut_user_av,
                            dut_passwd_av, dia_username_av, dia_passwd_av)
        curtime = str(time.strftime('%Y%m%d', time.localtime()))
        table_name = 'av_' + curtime
        table_name = table_name.encode('utf-8')

        tn.write(b'truncate ' + table_name + b';' + b'\n')
        time.sleep(3)
        print('truncate table successed')
        tn.close()

    def dut_check_database(self, dut_version='R2.2SP'):
        '''
        检查数据库中已经产生的AV日志
        '''
        tn = self._conn_dut(dut_host_av, dut_user_av,
                            dut_passwd_av, dia_username_av, dia_passwd_av)
        curtime = str(time.strftime('%Y%m%d', time.localtime()))
        table_name = 'av_' + curtime
        table_name = table_name.encode('utf-8')

        tn.write(b'select * from ' + table_name + b';' + b'\n')
        msg = tn.read_until(b'mysql>', 10)
        msg = msg.decode('utf-8')
        test_result = open('av_detect_results_%s_%s.txt' %
                           (curtime, dut_version), 'w')
        with open('list.txt', 'r') as f:
            n = 0
            total = 100
            for line in f:
                line = line.strip('\n')
                namere = re.compile(r'%s' % line)
                if namere.search(str(msg)):
                    test_result.write(str(line) + ' ' + 'OK' + '\n')
                    n += 1
                else:
                    test_result.write(str(line) + ' ' + 'POK' + '\n')
            test_result.write(
                ('The AV module detect result: %d OK, %d POK' % (n, total - n)) + '\n')
        test_result.close()
        time.sleep(3)
        tn.close()


def main():
    '''
    执行测试
    '''
    test = AV_Sample_AutoTest()
    test.dut_del_database()
    test.get_avfile_http()
    time.sleep(10)
    test.dut_check_database()


if __name__ == '__main__':
    main()
