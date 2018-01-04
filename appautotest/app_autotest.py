# -*- coding: utf-8 -*-

import re
import time
import sys
import encodings
import telnetlib
import csv

import pymysql
import requests

from configure_all import *


class WebApp_AutoTest(object):

    def __init__(self):
        pass

    def _conn_mysql(self):
        '''
        连接数据库
        '''
        conn = pymysql.connect(host=mysql_host, user=mysql_user,
                               password=mysql_passwd, db=mysql_db, port=3306)
        return conn

    def _conn_dut(self, host, username, passwd):
        '''
        telnet连接DUT
        '''
        print('telnet to dut:%s' % host)
        host = host.encode('utf-8')
        username = username.encode('utf-8')
        passwd = passwd.encode('utf-8')

        tn = telnetlib.Telnet(host, port=23, timeout=10)
        tn.read_until('Username:'.encode('utf-8'))
        tn.write(username + b'\n')
        tn.read_until(b'Password:')
        tn.write(passwd + b'\n')
        tn.read_until(b'>', 10)
        print('telnet successed, continue...')
        tn.write(b'enable' + b'\n')
        return tn

    def get_app_data(self):
        '''
        从数据库表中获取app的id
        '''
        print('connect to mysql server \'%s\'' % mysql_host)
        db1 = self._conn_mysql()
        cur = db1.cursor()
        sql = "SELECT * FROM `applications` WHERE `category` = 'websites' AND `enable` = 2"
        app_data = {}
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                appid = row[1]
                name_en = row[2]
                name_cn = row[3]
                refer = row[6]
                app_data.setdefault(appid, []).append(name_en)
                app_data.setdefault(appid, []).append(refer)
            return app_data
        except Exception as e:
            raise e
        finally:
            db1.close()

    def webapp_request(self, refer):
        '''
        使用第三方库request发送请求,根据response的数据进行判断DUT是否成功阻断请求并返回，有以下几种返回：
        1、deny:被DUT阻断了
        2、allow:请求成功了，可以认为DUT没有阻断这次请求，有可能
        3、error:当前只对10060错误码进行了捕获并详细返回，可能原因为referer是错误的
        4、返回抛出的异常信息：其他错误码均把抛出的异常返回
        '''
        re_http_refer = re.compile(r'http')
        re_https_refer = re.compile(r'https')

        if re_http_refer.search(refer):
            try:
                print('sending http request by lib of Request')
                rq = requests.get(refer)
                rq.encoding = 'utf-8'
                re_fw_text = re.compile(r'违反了相关的访问限制')
                if re_fw_text.search(rq.text):  # 增加清流操作
                    print('DUT deny the http request')
                    return 'deny'
                else:
                    print('send http request and resieve response success')
                    return 'allow'
            except Exception as e:
                re_errorcode0 = re.compile(r'10060')  # 连接服务器失败返回的错误码
                if re_errorcode0.search(str(e)):
                    print('connect error, maybe the referer is error')
                    return 'error'
                else:
                    print('connect error, unknown error')
                    return str(e)
        if re_https_refer.search(refer):
            try:
                print('sending https request by lib of Request')
                rq = requests.get(refer)
            except Exception as e:
                re_errorcode1 = re.compile(r'10054')  # DUT阻断返回的错误码
                re_errorcode2 = re.compile(r'10060')  # 连接服务器失败返回的错误码
                if re_errorcode1.search(str(e)):
                    print('DUT deny the https request')
                    return 'deny'
                if re_errorcode2.search(str(e)):
                    print('Something error, maybe the referer is error!')
                    return 'error'
                else:
                    print('connect error, unknown error')
                    return str(e)
            print('send https request and resieve response success')
            return 'allow'

    def dut_add_conf(self, appname, ruleid='8', action='deny'):
        '''
        policy中添加app规则
        '''
        tn = self._conn_dut(dut_host, dut_user, dut_passwd)
        appname = appname.encode('utf-8')
        action = action.encode('utf-8')
        ruleid = ruleid.encode('utf-8')

        tn.read_until(b'host#')
        tn.write(b'conf t' + b'\n')
        print('add app rule...')
        tn.read_until(b'#', 10)
        tn.write(b'app-policy 31' + b'\n')
        tn.read_until(b'#', 10)
        tn.write(b'rule %s %s any any include any always %s alerts' %
                 (ruleid, appname, action) + b'\n')
        tn.read_until(b'#', 10)
        print('add app rule %d successed, continue...' % int(ruleid))
        tn.write(b'end' + b'\n')
        tn.read_until(b'#', 10)
        time.sleep(3)
        tn.close()

    def dut_del_conf(self, ruleid='8'):
        '''
        policy中删除app规则
        '''
        tn = self._conn_dut(dut_host, dut_user, dut_passwd)
        ruleid = ruleid.encode('utf-8')

        tn.read_until(b'host#')
        tn.write(b'conf t' + b'\n')
        print('del app rule...')
        tn.read_until(b'#', 10)
        tn.write(b'app-policy 31' + b'\n')
        tn.read_until(b'#', 10)
        tn.write(b'no rule %s' % ruleid + b'\n')
        tn.read_until(b'#', 10)
        print('del app rule %d successed, continue...' % int(ruleid))
        tn.write(b'end' + b'\n')
        tn.read_until(b'#', 10)
        time.sleep(3)
        tn.close()

    def dut_check_app_recog(self):
        pass

    def dut_check_app_log(self):
        pass


def main():
    '''
    执行测试
    '''
    app = WebApp_AutoTest()
    appdata = app.get_app_data()
    ct = str(time.strftime('%Y%m%d%H%M%S', time.localtime()))
    # newline=''是在python3中增加的避免空行的参数，如果是python2可以将打开方式设置为'wb'来避免空行
    test_result_file = open('test_result_file_%s.csv' % ct, 'w', newline='')
    writer = csv.writer(test_result_file)
    file_header = ['appid', 'appname', 'result', 'info']
    writer.writerow(file_header)
    # for id in appdata:
    for id in (2522, 2524, 2525, 2526):
        appname = appdata[id][0]
        webrefer = appdata[id][1]  # http测试
        # webrefer = appdata[id][1] #https测试
        # restr = re.compile(r'http')
        # webrefer = restr.sub('https', webrefer)
        print('clear the DUT configure')
        app.dut_del_conf()
        print('start testing web applications, appid:%s appname:%s' %
              (id, appname))
        app.dut_add_conf(appname)
        test_result = app.webapp_request(webrefer)
        if test_result == 'deny':
            app.dut_del_conf()
            test_result_second = app.webapp_request(webrefer)
            if test_result_second == 'allow':
                info = 'test OK!'
                print(info)
                writer.writerow([str(id), appname, 'ok', info])
            else:
                info = 'test Faild, can not connect to the web server!'
                print(info)
                writer.writerow([str(id), appname, 'pok', info])
            continue
        if test_result == 'allow':
            info = 'DUT did not deny the https request, please check the configure or signature!'
            print(info)
            writer.writerow([str(id), appname, 'pok', info])
            continue
        if test_result == 'error':
            info = 'Test Faild, can not connect to the web server!'
            print(info)
            writer.writerow([str(id), appname, 'pok', info])
            continue
        else:
            info = 'Test Faild, unknown error!'
            print(info)
            writer.writerow([str(id), appname, 'pok', info])
        time.sleep(5)
    test_result_file.close()


if __name__ == '__main__':
    main()
