# -*- coding: utf-8 -*-

import sys
import encodings
import telnetlib
import re
import time
import pymysql
from selenium import webdriver
from configure_all import *


class App_Autotest(object):

    def __init__(self):
        pass

    def _conn_mysql(self):
        print('connect to mysql server')
        conn = pymysql.connect(host=mysql_host, user=mysql_user,
                               password=mysql_passwd, db=mysql_db, port=3306)
        return conn

    # def _unicode_to_utf8(self, unistr):
    #     print(type(unistr))
    #     return self.decode(unistr)
    #     # return unistr.encode('utf-8')

    def _check_http_response(self, response):
        '''
        检查页面返回的数据是否与预期一致
        '''
        pass

    def get_appname(self, appid):
        '''
        连接数据库，从表中获取app的英文名称
        '''
        db1 = self._conn_mysql()
        cur = db1.cursor()
        sql = "SELECT * FROM `applications` WHERE `app_id` = '%s'" % appid
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                id = row[0]
                appid = row[1]
                name_en = row[2]
                refer = row[6]
                return name_en
        except Exception as e:
            raise e
        finally:
            print('close the connection of mysql')
            db1.close()

    def get_apprefer(self, appid):
        '''
        连接数据库，从表中获取app的网站referer
        '''
        db1 = self._conn_mysql()
        cur = db1.cursor()
        sql = "SELECT * FROM `applications` WHERE `app_id` = '%s'" % appid
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                id = row[0]
                appid = row[1]
                name_en = row[2]
                refer = row[6]
                return refer
        except Exception as e:
            raise e
        finally:
            print('close the connection of mysql')
            db1.close()

    def webapp_open(self, refer):
        browser = ''
        implicitly_wait = 5
        print('open chrome browser')
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(implicitly_wait)
        print("browser open url %s" % refer)
        self.browser.get(refer)
        self.browser.refresh()
        time.sleep(5)
        self.browser.quit()
        print("close browser")

    def dut_conn(self, host, username, passwd, appname, ruleid, action='deny'):
        print('telnet to dut:%s' % host)
        host = host.encode('utf-8')
        username = username.encode('utf-8')
        passwd = passwd.encode('utf-8')
        appname = appname.encode('utf-8')
        action = action.encode('utf-8')
        ruleid = ruleid.encode('utf-8')

        tn = telnetlib.Telnet(host, port=23, timeout=10)
        tn.read_until('Username:'.encode('utf-8'))
        tn.write(username + b'\n')
        tn.read_until(b'Password:')
        tn.write(passwd + b'\n')
        tn.read_until(b'>', 10)
        print('telnet successed!')
        tn.write(b'enable' + b'\n')
        tn.read_until(b'host#')
        tn.write(b'conf t' + b'\n')
        print('add app rule...')
        tn.read_until(b'#', 10)
        tn.write(b'app-policy 2' + b'\n')
        tn.read_until(b'#', 10)
        # tn.write(b'no rule 1' + b'\n')
        tn.write(b'rule %s %s any any include any always %s alerts' %
                 (ruleid, appname, action) + b'\n')
        tn.read_until(b'#', 10)
        print('add successed!')
        tn.write(b'end' + b'\n')
        tn.read_until(b'#', 10)
        time.sleep(3)
        print('disconnect!')
        tn.close()

    def dut_add_conf(self):
        pass

    def dut_check_conf(self):
        pass

    def dut_del_conf(self):
        pass

    def dut_check_app_recog(self):
        pass

    def dut_check_app_log(self):
        pass


if __name__ == '__main__':
    # pass
    a = App_Autotest()
    ruleid = '1'
    for id in [1476, 1498, 2795]:
        print(ruleid)
        print('id:%s appname:%s' % (id, a.get_appname(id)))
        a.dut_conn(dut_host, dut_user, dut_passwd, a.get_appname(id), ruleid)
        ruleid = str(int(ruleid) + 1)
        # a.webapp_open(a.get_apprefer(id))
