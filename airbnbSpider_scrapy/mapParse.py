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
import requests
import scrapy
from lxml import etree
from requests.adapters import HTTPAdapter
from multiprocessing import Process
from multiprocess import Pool


class mapParse():
    def __init__(self):
        self.table = "`airbnbspider`.`proxypool`"
        self.db = pymysql.connect(
            "localhost", "root", "delta=b2-4ac", "airbnbspider")
        self.cursor = self.db.cursor()
        self.mapTable = "`airbnbspider`.`map`"
        self.listTable = "`airbnbspider`.`houselist`"
        self.mapresponseTable = "`airbnbspider`.`mapresponse`"

    def getItem(self,bias):
        sql = "SELECT * FROM "+ self.mapresponseTable +"WHERE id between {} and {}".format(bias,bias+100)
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        for row in results:
            res = row[1].replace("''", "'")
            res = res.replace('""', '"')
            try:
                res = json.loads(res, strict=False)
            except:
                print("err in {}".format(row[0]))
                return
            print("handleing  {}".format(row[0]))
            if 'home_tab_metadata' in res['explore_tabs'][0]:
                count = res['explore_tabs'][0]['home_tab_metadata']['listings_count']
                sections = res['explore_tabs'][0]['sections']
                for section in sections:
                    self.exist = 0
                    self.insert = 0
                    if 'listings' in section:
                        self.inDB = ""
                        listings = section['listings']
                        for listing in listings:
                            try:
                                self.decodeListing(listing)
                            except Exception as e:
                                print(str(e), "for listing", time.asctime(
                                    time.localtime(time.time())))

                        print(" count;{}   共{}个，其中重复{}，新增{},{}".format(
                             count, str(len(listings)), self.exist, self.insert, self.inDB))
            else:
                print("房源list解码异常")
                self.dbUpdateStates("done")

    def dbMapUpdateStates(self, state):
        sql = "UPDATE "+self.mapTable + \
            " SET `state`='{}' WHERE `id`='{}'".format(state, self.id)
        self.cursor.execute(sql)
        self.db.commit()

    def dbHouseExist(self, house_id):
        sql = "SELECT * FROM "+self.listTable + \
            "WHERE house_id = {}".format(house_id)
        self.cursor.execute(sql)
        self.db.commit()
        if(len(self.cursor.fetchall()) >= 1):
            return True
        else:
            return False

    def dbHouseInsert(self, price, description, house_id):
        sql = "INSERT INTO " + self.listTable + " VALUES (NULL ,'{}','{}','{}','{}')".format(
            price, description, house_id,123)
        # print(sql)
        self.cursor.execute(sql)
        self.db.commit()

    def decodeListing(self, listing):
        price = listing['pricing_quote']['price_string']
        description = listing['listing']['name']
        house_id = listing['listing']['id']
        # print(house_id)
        description = description.replace("'", "''")
        description = description.replace('"', '""')
        if(self.dbHouseExist(house_id)):
            # self.dbHouseInsert(price,description,house_id)
            self.exist += 1
            self.inDB += "-"
        else:
            self.dbHouseInsert(price, description, house_id)
            self.insert += 1
            self.inDB += "&"

sm = threading.Semaphore(40)

def parseStart(bias):
    parse = mapParse()
    parse.getItem(bias*100)
    sm.release()

if __name__ == "__main__":

    # i=range(0,5000)
    # pool=Pool(40)

    # pool.map(parseStart,i)

    # pool.close()
    # pooo.join()

    for i in range(0,500):
        sm.acquire()
        time.sleep(0.05)
        th = threading.Thread(target=parseStart, args=(i,))
        th.start()


