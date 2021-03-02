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

def getOrder(listingId):
    results = dbUtils("SELECT * FROM `order` WHERE `house_id` = {}".format(listingId))
    


if __name__ == "__main__":
    listingIds = [45917271, 40658820, 44546841, 36491415, 38033861, 14363531, 46983891, 34193677, 47110001, 37866069]
