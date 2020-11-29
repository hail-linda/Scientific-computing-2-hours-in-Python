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

from itertools import cycle
col_gen = cycle('bgrcmk')

db = pymysql.connect("localhost","root","delta=b2-4ac","spideairbnb" )
cursor = db.cursor()

sql = "SELECT * FROM spideairbnb.numofhousesavailable where num < 50 and num > 0"
cursor.execute(sql)
results = cursor.fetchall()
'''
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
    #if(row[5]<50):
    #    ax.text((row[4]+row[3])/2,(row[2]+row[1])/2,row[5])
'''
X=[]
Y=[]
S=[]
C=[]
for row in results:
    X.append((row[4]+row[3])/2)
    Y.append((row[2]+row[1])/2)
    S.append(row[5])
    C.append(((row[5]/50),(row[5]/50),0))

X=np.array(X)
Y=np.array(Y)
S=np.array(S)
C=np.array(C)


plt.scatter(X,Y,s=S,c=C,alpha=0.2,linewidths=0)
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


plt.show()







