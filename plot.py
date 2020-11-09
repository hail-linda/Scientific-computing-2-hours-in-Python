# -*- coding: UTF-8 -*-

import json
import re
import sqlite3
import pymysql
import threading
import time
from threading import Semaphore, Thread

import chardet
import lxml
import requests
import scrapy
from lxml import etree
from requests.adapters import HTTPAdapter

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes

import numpy as np

from itertools import cycle
col_gen = cycle('bgrcmk')

db = pymysql.connect("localhost","root","delta=b2-4ac","spideairbnb" )
cursor = db.cursor()

sql = "SELECT * FROM `spideairbnb`.`numofhousesavailable`"
cursor.execute(sql)
results = cursor.fetchall()

fig,ax = plt.subplots()
for row in results:
    xy = np.array([row[3],row[1]])
    rect = mpathes.Rectangle(   xy = xy,
                                width = row[4]-row[3],
                                height = row[2]-row[1],
                                edgecolor='blue',
                                fill = False,
                                linewidth=1)
    ax.add_patch(rect)
    if(row[5]<300):
        ax.text((row[4]+row[3])/2,(row[2]+row[1])/2,row[5])

plt.axis('equal')


plt.show()







