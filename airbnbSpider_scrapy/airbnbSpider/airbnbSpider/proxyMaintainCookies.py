# -*- coding: UTF-8 -*-

import json
import random
import re
import sqlite3
import threading
import time
from threading import Semaphore, Thread
import datetime

import chardet
import lxml
import pymysql

import dbSettings
import requests
import scrapy
from lxml import etree
from requests.adapters import HTTPAdapter

from SMTP import SMTP


class proxyPool:
    def __init__(self):
        self.proxyId = 0
        self.ip = ""
        self.table = "`proxypool`"
        self.db = dbSettings.db_connect()
        self.cursor = self.db.cursor()

    def dbInsert(self, proxy, cookies):
        sql = "INSERT INTO "+self.table + \
            " (`ip`, `numused`, `state`,`cookies`) VALUES ('{}', '0', 'new','{}')".format(
                proxy, cookies)
        self.cursor.execute(sql)
        self.db.commit()

    def dbUpdateCookies(self, row, proxy):
        # UPDATE runoob_tbl SET runoob_title='学习 C++' WHERE runoob_id=3;
        sql = "UPDATE "+self.table + "SET cookies = '" + \
            proxy + "' WHERE id = " + str(row['id'])
        self.cursor.execute(sql)
        self.db.commit()
        print("update cookies", row['id'])

    def IP(self):
        sql = "SELECT * from "+self.table+"WHERE `state` != 'del'"
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        if(len(results) < 5):
            pass
            # self.get()
            time.sleep(2)
            return self.IP()
        rand = random.randint(0, len(results)-1)
        # print(results[rand])
        self.ip = results[rand][1]
        self.proxyId = results[rand][0]

        sql = "UPDATE "+self.table + \
            " SET `numused` = `numused` + 1 WHERE `id` = " + \
            str(results[rand][0])
        self.cursor.execute(sql)
        self.db.commit()

        return self.IP

    def proxies(self):
        self.IP()
        self.proxies = {
            "http": " http://{}".format(self.ip),
            "https": "https://{}".format(self.ip),
        }
        return self.proxies

    def checkBalance(self):
        orderid = "931589300651176"
        url = "http://dps.kdlapi.com/api/getipbalance?orderid={}&signature=0s8l8934i0kp26l8ox8h4aalero7cxxj".format(
            orderid)
        proxies = {"http": None, "https": None}
        html = requests.get(url, timeout=5, proxies=proxies)
        res = json.loads(html.content)
        print(res)
        return res['data']['balance']

    def get(self, num=20):
        orderid = "931589300651176"
        url = "http://dps.kdlapi.com/api/getdps/?orderid={}&num={}&pt=1&format=json&sep=1&dedup=1".format(
            orderid, str(num))
        print(url)
        proxies = {"http": None, "https": None}
        html = requests.get(url, timeout=5, proxies=proxies)

        # print(html)
        res = json.loads(html.content)
        print("get proxy ", time.asctime(
            time.localtime(time.time())))
        if 'data' in res:
            res = res['data']
        else:
            print("get proxy err in data")
        count = res['count']

        if 'proxy_list' in res:
            proxys = res['proxy_list']
        else:
            print("get proxy err in proxy_list")

        for proxy in proxys:
            # rootCookies = self.getCookies("https://www.airbnb.cn",proxy)
            pgPixelCookies = self.getCookies(
                "https://www.airbnb.cn/pg_pixel?r=&diff=16115071061939667863691016617", proxy)
            acwCookies = pgPixelCookies + self.acw_sc(proxy)
            # acwCookies = pgPixelCookies
            self.dbInsert(proxy, acwCookies)

    def acw_sc(self,proxy):
        base_url = 'https://www.airbnb.cn/api/v3/PdpAvailabilityCalendar?operationName=PdpAvailabilityCalendar&locale=zh&currency=CNY&_cb=d2yi4563zcoq&variables=%7B%22request%22%3A%7B%22count%22%3A12%2C%22listingId%22%3A%2243502836%22%2C%22month%22%3A5%2C%22year%22%3A2021%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22dc360510dba53b5e2a32c7172d10cf31347d3c92263f40b38df331f0b363ec41%22%7D%7D'
        arg1 = self.get_script_data(base_url,proxy = proxy)
        # arg1 = "BC5F184213CAF358078C4DC21664A8D6830567AA"
        _0x23a392 = self.unsbox(arg1)
        arg2 = 'acw_sc__v2=' + self.hexXor(_0x23a392)
        print(arg2)

        while(1):
            base_url = 'https://www.airbnb.cn/api/v3/PdpAvailabilityCalendar?operationName=PdpAvailabilityCalendar&locale=zh&currency=CNY&_cb=d2yi4563zcoq&variables=%7B%22request%22%3A%7B%22count%22%3A12%2C%22listingId%22%3A%2246903886%22%2C%22month%22%3A5%2C%22year%22%3A2021%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22dc360510dba53b5e2a32c7172d10cf31347d3c92263f40b38df331f0b363ec41%22%7D%7D'
            try:
                arg1 = self.get_script_data(base_url,self.hexXor(_0x23a392),proxy = proxy)
            except Exception as e:
                print(arg2,e)
                break
            # arg1 = get_script_data(base_url,hexXor(_0x23a392))
            # arg1 = "AF383E77A68EAA57773646A22DB6AF37B9015206"
            _0x23a392 = self.unsbox(arg1)
            arg2 = 'acw_sc__v2=' + self.hexXor(_0x23a392)
            print(arg2)
            print(self.hexXor(_0x23a392))
        return arg2

    def updateCookies(self, row):
        proxy = row['ip']
        rootCookies = self.getCookies("https://www.airbnb.cn", proxy)
        pgPixelCookies = self.getCookies(
            "https://www.airbnb.cn/pg_pixel?r=&diff=16115071061939667863691016617", proxy, rootCookies)
        acw_sc__v2 = self.acw_sc()
        pgAcwPixelCookies = pgPixelCookies + acw_sc__v2
        self.dbUpdateCookies(row, pgPixelCookies)

    def getCookies(self, url, proxy, srcCookies=""):
        headers = {"cookies": srcCookies}
        username = "1282255404"
        password = "123456"
        proxies = {
            "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy},
            "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy}
        }
        res = requests.get(url, headers=headers,proxies = proxies)
        # print(res.cookies)
        rootCookies = srcCookies
        for key, value in res.cookies.items():

            print(str(key))
            if  str(key) == "acw_tc__v2" or str(key) == "bev":
                rootCookies = rootCookies + str(key)+"="+str(value)+";"
                print(key + "=" + value)
        return rootCookies

    def delete(self, delReason):
        sql = "UPDATE "+self.table + \
            " SET `state` = 'del' WHERE `id`='{}'".format(self.proxyId)
        self.cursor.execute(sql)
        self.db.commit()
        sql = "UPDATE "+self.table + \
            " SET `delreason` = '{}' WHERE `id`='{}'".format(
                delReason, self.proxyId)
        self.cursor.execute(sql)
        self.db.commit()

    def get_script_data(self,base_url,acw = "",proxy = ""):
        '''
        获取js相应参数
        '''
        username = "1282255404"
        password = "123456"
        proxies = {
            "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy},
            "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy}
        }
        headers = {
        'X-Airbnb-API-Key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20',
        'Cookie': 'acw_sc__v2='+acw
        }
        print(headers)


        response = requests.get(base_url, headers=headers,proxies = proxies)
        print(response.text[:400])
        arg1 = re.search("arg1='([^']+)'", response.text).group(1)
        return arg1

    def unsbox(self,arg1):
        box = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19, 0xd, 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c, 0x22, 0x25, 0xc, 0x24]
        res = list(range(0, len(arg1)))
        for i in range(0, len(arg1)):
            j = arg1[i]
            for k in range(0, 40):
                if box[k] == i+1:
                    res[k] = j
        res = "".join(res)
        return res

    def hexXor(self,arg2):
        box = "3000176000856006061501533003690027800375"
        res = ""
        for i in range(0, 40, 2):
            arg_H = int(arg2[i:i+2], 16)
            box_H = int(box[i:i+2], 16)
            res += hex(arg_H ^ box_H)[2:].zfill(2)
        # print(res)
        return res


def getIp():
    db = dbSettings.db_connect()
    cursor = db.cursor()
    timeNow = datetime.datetime.now()
    proxypool = proxyPool()
    while(1):
        time.sleep(1)
        sql = "SELECT * from `proxypool` WHERE `state` != 'del'"
        cursor.execute(sql)
        db.commit()
        results = cursor.fetchall()
        n_ip_kuaidaili = proxypool.checkBalance()
        if n_ip_kuaidaili == 0:
            SMTP("1282255404@qq.com", "发信内容", "快代理ip数耗尽警告", "DaduosuMonitor")
            time.sleep(180)
        print("test ip pool ,n_ip_proxypool: {} , n_ip_kuaidaili: {}".format(
            len(results), n_ip_kuaidaili))
        if(len(results) < 5):
            proxies = proxypool.get(num=3)
        for row in results:
            deltaTime = (timeNow - row['init_time']).seconds


if __name__ == "__main__":
    getIp()
