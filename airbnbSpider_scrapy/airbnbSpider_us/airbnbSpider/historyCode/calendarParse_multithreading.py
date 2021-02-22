# -*- coding: UTF-8 -*-

from multiprocessing import Process, Pool
import os
import time
import random

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
from multiprocessing import Process
from multiprocess import Pool


class calendarParse():
    def __init__(self):
        self.table = "`proxypool`"
        self.db = dbSettings.db_connect()
        self.cursor = self.db.cursor()
        self.mapTable = "`map`"
        self.listTable = "`houselist`"
        self.mapresponseTable = "`mapresponse`"
        self.calendarresponseTable = "`calendarresponse`"

        localtime = time.localtime(time.time())
        self.mouth = localtime[1]
        self.year = localtime[0]
        self.day = localtime[2]
        self.dtToday = "{}-{}-{}".format(self.year, self.mouth, self.day)

        self.orderList = []
        self.priceList = []
        self.house_id = 0

    def __del__(self):
        self.db.close()

    def dateCompare(self, dt1, dt2):
        dt1 = time.mktime(time.strptime(dt1, '%Y-%m-%d'))
        dt2 = time.mktime(time.strptime(dt2, '%Y-%m-%d'))
        return dt1-dt2

    def getItem(self, bias):
        sql = "SELECT * FROM " + self.calendarresponseTable + \
            "WHERE id between {} and {}".format(bias, bias+10)
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        for row in results:
            self.sqlId = row["id"]
            self.house_id = row["house_id"]
            res = row["response"].replace("''", "'")
            res = res.replace('""', '"')
            if "429 Too Many" in res:

                print("429 err in ", row["id"])
                continue
            # print(res)
            try:
                res = json.loads(res, strict=False)
            except Exception as e:
                print(e)
                print("json.loads err in {}".format(row["id"]))
                sql = "INSERT INTO `calendarparselog` ( `type`, `infor`)\
                 VALUES ('{}','{}');".format(row["id"], "429 err")
                self.cursor.execute(sql)
                self.db.commit()
                continue

            # if 'metadata' in res:
            #     if not 'first_bookable_day' in res['metadata']:
            #         return
            num = 0
            if 'calendar_months' in res:
                for month in res['calendar_months']:
                    for day in month['days']:
                        if self.dateCompare(self.dtToday, day['date']) < 0:
                            try:
                                self.priceList.append(
                                    [day['date'], day['price']['local_price_formatted']])
                                if day['available'] == False:
                                    self.orderList.append(day['date'])
                            except:
                                continue

        self.dbInsert()
        self.priceList = []
        self.orderList = []

    def dbInsert(self):
        self.vals = []
        self.sql = "INSERT IGNORE INTO `order` (`house_id`, `fetch_date`, `order_date`, `hash`)\
                 VALUES (%s,%s,%s,%s);"
        for order in self.orderList:
            hash = "{}:{}`".format(self.house_id, order)
            # print(self.house_id,self.dtToday,order,hash)
            self.vals.append((self.house_id, self.dtToday, order, hash))

        self.cursor.executemany(self.sql, self.vals)
        self.db.commit()
        self.orderAffected = self.cursor.rowcount

        self.vals = []
        self.sql = "INSERT IGNORE INTO `price` (`house_id`, `fetch_date`, `order_date`,`price`, `hash`)\
                 VALUES (%s,%s,%s,%s,%s);"

        for price in self.priceList:
            orderDate = price[0]
            price = price[1]
            hash = "{}:{}:{}".format(self.house_id, orderDate, price)
            self.vals.append(
                (self.house_id, self.dtToday, orderDate, price, hash))

        self.cursor.executemany(self.sql, self.vals)
        self.db.commit()
        self.priceAffected = self.cursor.rowcount

        # print("sqlId:{}\thouse_id: {}\t order insert {} in {} \tprice insert {} in {} \
        #     ".format(self.sqlId,self.house_id,self.orderAffected,len(self.orderList),self.priceAffected,len(self.priceList)))


sm = threading.Semaphore(1)


def parseStart(bias):
    # parse = calendarParse()
    # parse.getItem(bias*10)
    # sm.release()
    # return
    try:
        parse = calendarParse()
        parse.getItem(bias*10)
    except Exception as e:
        print(e)
        try:
            parse = calendarParse()
            parse.getItem(bias*10)
        except:
            try:
                parse = calendarParse()
                parse.getItem(bias*10)
            except Exception as e:
                print(e)
                print("err in {}".format(bias))

                pass

    sm.release()
    db = dbSettings.db_connect()
    cursor = db.cursor()
    sql = "INSERT INTO `calendarparselog` ( `type`, `infor`)\
            VALUES ('{}','{}');".format("start parse", bias*10)
    print(sql)
    cursor.execute(sql)
    db.commit()

if __name__ == "__main__":
    # parseStart(0)
    db = dbSettings.db_connect()
    cursor = db.cursor()
    sql = "SELECT id FROM `calendarresponse` order by id desc limit 20"
    cursor.execute(sql)
    db.commit()
    num = cursor.fetchall()[0]["id"]

    sql = "SELECT * FROM `calendarparselog` order by id desc limit 20"
    cursor.execute(sql)
    db.commit()
    try:
        start = cursor.fetchall()[0]["infor"]
    except:
        start = 25600

    print(int(start)*10)

    print("start parse at ".format(int(start)*10))

    for i in range(round(int(start)/10), round(num/10)+1):
        sm.acquire()
        time.sleep(0.05)
        th = threading.Thread(target=parseStart, args=(i,))
        th.start()
