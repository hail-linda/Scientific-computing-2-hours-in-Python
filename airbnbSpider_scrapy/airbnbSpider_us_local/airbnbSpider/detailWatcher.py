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


class watcher():
    def __init__(self):
        self.table = "`proxypool`"
        self.db = dbSettings.db_connect()
        self.cursor = self.db.cursor()
        self.mapTable = "`map`"
        self.listTable = "`houselist`"
        self.mapresponseTable = "`mapresponse`"

    def run(self):
        sql = "SELECT MAX(id) FROM detailresponse"
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        return results[0]["MAX(id)"] 

   

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





