# -*- coding: utf-8 -*-

import sys
import time
import pymysql
from configure_all import *


class IPS_Autopack(object):
    """
    1.select 5 items from db for release;
    """

    def __init__(self):
        pass

    def _conn_mysql(self):
        conn = pymysql.connect(host=mysql_host, user=mysql_user,
                               password=mysql_passwd, db=mysql_db, port=3306)
        return conn

    def get_value(self, tablename, id):
        '''
        连接数据库，从表中返回指定id的ips事件信息
        '''
        db1 = self._conn_mysql()
        cur = db1.cursor()
        sql = "SELECT * FROM `%s` WHERE `id` = '%s'" % (tablename, id)
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                id = row[0]
                if tablename == 'ips_events':
                    ips_post_status = row[2]
                    enable = row[3]
                    decode_match = row[4]
                elif tablename == 'ips_events_new':
                    ips_post_status = row[3]
                    enable = row[4]
                    decode_match = row[5]
                if (ips_post_status == 1) or (enable == 0) or (decode_match == ''):
                    return None
                else:
                    return {'id': id, 'ips_post_status': ips_post_status, 'enable': enable, 'decode_match': decode_match}
        except Exception as e:
            raise e
        finally:
            db1.close()


if __name__ == '__main__':

    trav_old = IPS_Autopack()
    id_for_oldrel = []
    for id in range(3122, 3127):
        if trav_old.get_value('ips_events', id) != None:
            id_for_oldrel.append(id)
            print(trav_old.get_value('ips_events', id))
    print('oldips:', id_for_oldrel)

    trav_new = IPS_Autopack()
    id_for_newrel = []
    for id in range(3040, 3048):
        if trav_new.get_value('ips_events_new', id) != None:
            id_for_newrel.append(id)
            print(trav_new.get_value('ips_events_new', id))
    print('newips:', id_for_newrel)
