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

def getListingId():
    db = dbSettings.db_connect()
    cursor = db.cursor()

    sql = "SELECT house_id FROM `houselist_us` ORDER BY RAND() LIMIT 100000"
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    return [i['house_id'] for i in result]


if __name__ == "__main__":
    f = open("houseId1M.txt", 'w')
    print(getListingId(),file=f)