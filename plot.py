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
import matplotlib.image as img

import numpy as np
import dbSettings

from itertools import cycle
col_gen = cycle('bgrcmk')

db = dbSettings.db_connect()
cursor = db.cursor()

sql = "SELECT * FROM airbnb_scrapy.map_us where num < 50 and num > 0"
cursor.execute(sql)
results = cursor.fetchall()
X=[]
Y=[]
S=[]
C=[]
for row in results:
    X.append((row['lon_upp']+row['lon_low'])/2)
    Y.append((row['lat_upp']+row['lat_low'])/2)
    S.append(row['num']/10)
    # C.append(((row['num']/80),(row['num']/80),0))
    C.append(row['num']/180.0)

X=np.array(X)
Y=np.array(Y)
S=np.array(S)
C=np.array(C)


plt.scatter(X,Y,s=S,c=C,alpha=0.2,linewidths=0, cmap='summer')
#plt.figure().figimage(img.imread('./china_map.jpg'))

'''
index=0
for row in results:
    index+=1
    if(index%400==0):
        print("{}/{}".format(index,len(results)))
    plt.scatter((row[4]+row[3])/2,(row[2]+row[1])/2,s=row[5],c=arctan2(50),alpha = .2)
'''


plt.axis('equal')

plt.savefig('./test.png',dpi=2000)
plt.show()







