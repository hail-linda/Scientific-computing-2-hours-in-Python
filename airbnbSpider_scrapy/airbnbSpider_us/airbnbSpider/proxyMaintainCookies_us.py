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


class proxyPool:
    def __init__(self):
        self.proxyId = 0
        self.ip = ""
        self.table = "`proxypool_us`"
        self.db = dbSettings.db_connect()
        self.cursor = self.db.cursor()

    def dbInsert(self, proxy,cookies):
        sql = "INSERT INTO "+self.table + \
            " (`ip`, `numused`, `state`,`cookies`) VALUES ('{}', '0', 'new','{}')".format(proxy,cookies)
        self.cursor.execute(sql)
        self.db.commit()

    def dbUpdateCookies(self,row,proxy):
        sql = "UPDATE "+self.table + "SET cookies = '" + proxy + "' WHERE id = " + str(row['id'])
        self.cursor.execute(sql)
        self.db.commit()
        print("update cookies",row['id'])
        
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
        orderid = "931589300651176"
        url = "http://dps.kdlapi.com/api/getdps/?orderid={}&num={}&pt=1&format=json&sep=1&dedup=1".format(orderid,str(num))
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
        rootCookies = self.getCookies("https://www.airbnb.com",proxys[0])
        getCookiesSuccessCount = num
        for proxy in proxys:
            try:
                pgPixelCookies = ""
                pgPixelCookies = self.getCookies("https://www.airbnb.com/pg_pixel?r=&diff=161728783672247040160844199774",proxy,rootCookies)
                print(proxy)
                self.dbInsert(proxy,pgPixelCookies)
                getCookiesSuccessCount -= 1
            except Exception as e:
                print(proxy," get cookies err: " ,e)
        if getCookiesSuccessCount > 5:
            quit()# try after 3 or 5 minutes

    def updateCookies(self,row):
        proxy = row['ip']
        rootCookies = self.getCookies("https://www.airbnb.com",proxy)
        pgPixelCookies = self.getCookies("https://www.airbnb.com/pg_pixel?r=&diff=161728783672247040160844199774",proxy,rootCookies)
        
        self.dbUpdateCookies(row,pgPixelCookies)

    def getCookies(self,url,proxy,srcCookies=""):
        username = "1282255404"
        password = "123456"
        proxies = {
            "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy},
            "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy}
        }
        # request.headers['Proxy-Authorization'] = "Basic MTI4MjI1NTQwNDoxMjM0NTY="
        headers = {"cookies" : srcCookies}
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=8))
        s.mount('https://', HTTPAdapter(max_retries=8))
        
        res = s.get(url,headers = headers, timeout=7,proxies = proxies)
        # print(res.cookies)
        rootCookies = srcCookies
        print(rootCookies)
        for key, value in res.cookies.items():
            # print(key + "=" + value)
            # print()
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
    timeNow = datetime.datetime.now()
    while(1):
        print("test ip pool")
        time.sleep(1)
        sql = "SELECT * from `proxypool_us` WHERE `state` != 'del'"
        cursor.execute(sql)
        db.commit()
        results = cursor.fetchall()
        if(len(results) < 10):
            proxypool = proxyPool()
            proxies = proxypool.get(num=10)
        for row in results:
            deltaTime = (timeNow - row['init_time']).seconds
            # if deltaTime < 600 :
            #     proxypool = proxyPool()
            #     proxypool.updateCookies(row)




if __name__ == "__main__":
    getIp()