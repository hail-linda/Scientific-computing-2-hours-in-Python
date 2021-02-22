# -*- coding: UTF-8 -*-

import os
import time
import random

import json
import re
import sqlite3
import threading
import time
from threading import Semaphore, Thread

import pymysql

import dbSettings
import requests

batchSize = 100000


def dbMoveOrder(batchFrom,db,cursor):
    sql = "SELECT * FROM `order` where id between {} and {}".format(batchFrom,batchFrom+batchSize)
    cursor.execute(sql)
    db.commit()
    results = cursor.fetchall()
    sql = "INSERT IGNORE INTO `order_` (`house_id`, `fetch_date`, `order_date`, repeat_flag)\
        VALUES (%s,%s,%s,%s);"

    vals = []
    for row in results :
        fetch_date = row["fetch_date"]
        order_date = row["order_date"]
        house_id = row["house_id"]
        repeat_flag = "{}:{}".format(house_id, order_date)
        vals.append(
                (house_id, fetch_date, order_date, repeat_flag))
                
    # print(vals)
    cursor.executemany(sql, vals)
    db.commit()


if __name__ == "__main__":
    db = dbSettings.db_connect()
    cursor = db.cursor()

    sql = "SELECT * FROM `order` order by id desc limit 1"
    cursor.execute(sql)
    db.commit()
    numTotal = cursor.fetchall()[0]["id"]
    print(numTotal)

    start = 0
    # numTotal = 20000

    for batchFrom in range(start,numTotal,batchSize):
        print(batchFrom,batchFrom+batchSize,100*batchFrom/numTotal)
        dbMoveOrder(batchFrom,db,cursor)
