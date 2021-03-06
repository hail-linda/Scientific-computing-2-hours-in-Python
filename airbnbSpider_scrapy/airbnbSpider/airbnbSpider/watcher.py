# -*- coding: UTF-8 -*-

import json
import random
import re
import threading
import redis , time
from threading import Semaphore, Thread

import chardet
import lxml
import pymysql

import dbSettings
from dbSettings import REDIS_URL
import requests


class watcher():
    def __init__(self):
        self.table = "`proxypool`"
        self.db = dbSettings.db_connect()
        self.cursor = self.db.cursor()
        self.redis = redis.Redis.from_url(REDIS_URL)
        self.mapTable = "`map`"
        self.listTable = "`houselist`"
        self.mapresponseTable = "`mapresponse`"

    def run(self):
        sql = "SELECT MAX(id) FROM calendarresponse"
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        return results[0]["MAX(id)"] 

    def checkRedis(self):
        return self.redis.llen("calendar:start_urls")

   

if __name__ == "__main__":
    w = watcher()
    sum20s = 0
    sum2min = 0
    index = 0
    while(1):
        index += 1
        num = w.run()
        time.sleep(1)
        n = w.run()-num
        redisLeft = w.checkRedis()
        sum20s += n
        sum2min += n
        print('redis:',redisLeft,'\t',n,'\t','*'*round(n/10))
        if(index % 20 == 0):
            print("20s avg:\t",sum20s/20.0)
            sum20s = 0
        if(index % 120 == 0):
            print("2min avg:\t",sum2min/120.0)
            sum2min = 0
            sum20s = 0
            index = 0





