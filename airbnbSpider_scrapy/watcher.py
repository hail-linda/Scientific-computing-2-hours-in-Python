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


class watcher():
    def __init__(self):
        self.table = "`airbnbspider`.`proxypool`"
        self.db = pymysql.connect(
            "localhost", "root", "delta=b2-4ac", "airbnbspider")
        self.cursor = self.db.cursor()
        self.mapTable = "`airbnbspider`.`map`"
        self.listTable = "`airbnbspider`.`houselist`"
        self.mapresponseTable = "`airbnbspider`.`mapresponse`"

    def run(self):
        sql = "SELECT COUNT(*) FROM airbnbspider.calendarresponse"
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        return results[0][0] 

   

if __name__ == "__main__":
    w = watcher()
    sum = 0
    index = 0
    while(1):
        index += 1
        num = w.run()
        time.sleep(1)
        n = w.run()-num
        sum += n
        print(n,'\t','*'*round(n/10))
        if(index == 20):
            print("avg:\t",sum/20.0)
            sum = 0
            index = 0





