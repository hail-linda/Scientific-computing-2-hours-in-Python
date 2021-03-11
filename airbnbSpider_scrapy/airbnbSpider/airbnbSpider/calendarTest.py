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

def dbUtils(sql):
    db = dbSettings.db_connect()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    return cursor.fetchall()

def getListingId():
    results = dbUtils("SELECT * FROM `houselist` ORDER BY RAND() LIMIT 10")
    return [i['house_id'] for i in result]

def getOrder():
    select = '`house_id` = 45917271 or `house_id` = 40658820 or `house_id` = 44546841 or `house_id` = 36491415 or `house_id` = 38033861 or `house_id` = 14363531 or `house_id` = 46983891 or `house_id` = 34193677 or `house_id` = 47110001 or `house_id` = 37866069'
    sql = "SELECT * FROM `order` WHERE id > 186941033 and ({})".format(select)
    print(sql)
    return dbUtils(sql)

def getPrice(listingId,date):
    sql = "SELECT price FROM `price` WHERE house_id = '{}' and order_date ='{}'".format(listingId,date)
    # print(sql)
    return dbUtils(sql)[0]['price']


if __name__ == "__main__":
    listingIds = [45917271, 40658820, 44546841, 36491415, 38033861, 14363531, 46983891, 34193677, 47110001, 37866069]
    results = getOrder()
    for row in results:
        print(row['house_id'],row['fetch_date'],row['order_date'],getPrice(row['house_id'],row['order_date']))
