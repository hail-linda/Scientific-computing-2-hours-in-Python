# -*- coding: UTF-8 -*-

import json
import random
import re
import sqlite3
import threading
import time
from threading import Semaphore, Thread

import chardet
import lxml
import pymysql

import dbSettings
import requests
import scrapy
from lxml import etree
from requests.adapters import HTTPAdapter


class proxyPool:
    def __init__(self):
        self.proxyId = 0
        self.ip = ""
        self.table = "`proxypool`"
        self.db = dbSettings.db_connect()
        self.cursor = self.db.cursor()

    def dbInsert(self, proxy,cookies):
        sql = "INSERT INTO "+self.table + \
            " (`ip`, `numused`, `state`,`cookies`) VALUES ('{}', '0', 'new','{}')".format(proxy,cookies)
        self.cursor.execute(sql)
        self.db.commit()

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

    def get(self, num=20):
        url = "http://dps.kdlapi.com/api/getdps/?orderid=941053123270010&num={}&pt=1&format=json&sep=1&dedup=1".format(str(num))
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
            rootCookies = self.getCookies("https://www.airbnb.cn",proxy)
            pgPixelCookies = self.getCookies("https://www.airbnb.cn/pg_pixel?r=&diff=16115071061939667863691016617",proxy,rootCookies)
            self.dbInsert(proxy,pgPixelCookies)
        
    def getCookies(self,url,proxy,srcCookies=""):
        proxies = {"http": " http://{}".format(proxy), "https": "https://{}".format(proxy),}
        headers = {"cookies" : srcCookies}

        res = requests.get(url,headers = headers)
        # print(res.cookies)
        rootCookies = srcCookies
        for key, value in res.cookies.items():
            print(key + "=" + value)
            print()
            rootCookies += str(key)+"="+str(value)+";"
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


def getIp():
    db = dbSettings.db_connect()
    cursor = db.cursor()
    while(1):
        print("test ip pool")
        time.sleep(0.5)
        sql = "SELECT * from `proxypool` WHERE `state` != 'del'"
        cursor.execute(sql)
        db.commit()
        results = cursor.fetchall()
        if(len(results) < 10):
            proxypool = proxyPool()
            proxies = proxypool.get(num=10)


if __name__ == "__main__":
    getIp()