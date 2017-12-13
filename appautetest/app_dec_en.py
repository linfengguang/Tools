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
                               password=mysql_passwd, db=mysql_db, port=3306, charset='utf8')
        return conn

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

    def get_appname_for_tab(self, tabname, valuelen, lan='en'):
        '''
        连接数据库，从表中获取指定长度的字段对应的app ID和name
        '''
        db1 = self._conn_mysql()
        cur = db1.cursor()
        sql = "SELECT * FROM `applications` WHERE LENGTH(%s)=%d" % (
            tabname, valuelen)
        try:
            cur.execute(sql)
            results = cur.fetchall()
            id = []
            appid = []
            name_en = []
            name_cn = []
            refer = []
            desc_en = []
            for row in results:
                id.append(row[0])
                appid.append(row[1])
                name_en.append(row[2])
                name_cn.append(row[3])
                desc_en.append(row[5])
                refer.append(row[6])
            print('the number of app:%s' % len(id))
            if lan == 'en':
                return name_en
            else:
                return name_cn
        except Exception as e:
            raise e
        finally:
            print('close the connection of mysql')
            db1.close()

    def get_desc_for_tab(self, tabname, valuelen, lan='cn'):
        '''
        连接数据库，从表中获取指定长度的字段对应的app ID和name
        '''
        db1 = self._conn_mysql()
        cur = db1.cursor()
        sql = "SELECT * FROM `applications` WHERE LENGTH(%s)=%d" % (
            tabname, valuelen)
        try:
            cur.execute(sql)
            results = cur.fetchall()
            id = []
            appid = []
            name_en = []
            name_cn = []
            refer = []
            desc_en = []
            desc_cn = []
            for row in results:
                id.append(row[0])
                appid.append(row[1])
                name_en.append(row[2])
                name_cn.append(row[3])
                desc_cn.append(row[4])
                desc_en.append(row[5])
                refer.append(row[6])
            print('the number of app:%s' % len(id))
            # print(name_cn)
            return desc_cn

        except Exception as e:
            raise e
        finally:
            print('close the connection of mysql')
            db1.close()

    def sig_locate(self, filename, keyword, offset=16):
        sig_str = ''
        data = open(filename, 'r', encoding='utf-8').readlines()
        for line in data:
            if (keyword in line.lower() and keyword == line[offset:-2].lower()) or (keyword.replace('-', '_') in line.lower() and keyword.replace('-', '_') == line[offset:-2].lower()):
                if data[data.index(line) + 2][4:15] == 'app_desc_en':
                    sig_str = data[data.index(line) + 2][offset:-2]
        return(sig_str)

    def desc_sig_locate(self, filename, keyword, offset=16):
        sig_str = ''
        data = open(filename, 'r', encoding='utf-8').readlines()
        for line in data:
            if keyword in line and keyword == line[offset:-2]:
                if data[data.index(line) + 1][4:15] == 'app_desc_en':
                    sig_str = data[data.index(line) + 1][offset:-2]
        return(sig_str)

    def update_table(self, tabname, keyvalue, appname_en):
        '''
        连接数据库，更新表中数据
        '''
        db1 = self._conn_mysql()
        cur = db1.cursor()
        sql = 'UPDATE applications SET %s = "%s" WHERE name_en ="%s"' % (
            tabname, keyvalue, appname_en)
        try:
            cur.execute(sql)
            db1.commit()
        except:
            db1.rollback()
            print('appname error, rollback!')
        finally:
            print('close the connection of mysql')
            db1.close()

    def update_table1(self, tabname, keyvalue, desc_cn):
        '''
        连接数据库，更新表中数据
        '''
        db1 = self._conn_mysql()
        cur = db1.cursor()
        sql = 'UPDATE applications SET %s = "%s" WHERE desc_cn ="%s"' % (
            tabname, keyvalue, desc_cn)
        try:
            cur.execute(sql)
            db1.commit()
        except:
            db1.rollback()
            print('desc error, rollback!')
        finally:
            print('close the connection of mysql')
            db1.close()


if __name__ == '__main__':
    a = App_Autotest()
    result_txt = open('result.txt', 'w')
    result_txt1 = open('result1.txt', 'w')
    newappname = {}
    newappname1 = {}
    for appname_en in a.get_appname_for_tab('desc_en', 256):
        if a.sig_locate('sap_apps_sigs.conf', appname_en) != '':
            newappname.setdefault(appname_en, a.sig_locate(
                'sap_apps_sigs.conf', appname_en).replace('%20', ' ').replace('"', ''))
    for desc_cn in a.get_desc_for_tab('desc_en', 256):
        if a.desc_sig_locate('sap_apps_sigs.conf', desc_cn) != '':
            newappname1.setdefault(desc_cn, a.desc_sig_locate(
                'sap_apps_sigs.conf', desc_cn).replace('%20', ' ').replace('"', ''))
    result_txt.write('已填充数据：' + '\n')
    for key in newappname:
        print(key)
        print(newappname[key])
        result_txt.write(key + '\n')
        result_txt.write(newappname[key] + '\n')
        a.update_table('desc_en', newappname[key], key)
    result_txt1.write('已填充数据：' + '\n')
    for key1 in newappname1:
        result_txt1.write(key1 + '\n')
        result_txt1.write(newappname1[key1] + '\n')
        a.update_table1('desc_en', newappname1[key1], key1)
    result_txt.close()
    result_txt1.close()
