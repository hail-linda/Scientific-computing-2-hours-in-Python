 # -*- coding: UTF-8 -*-

import sqlite3
import numpy as np
import requests,json,chardet
import time
from requests.adapters import HTTPAdapter
import threading
import scrapy,re
from lxml import etree
import lxml



def gethtml(url):
  i = 0
  while i < 3:
    try:
      html = requests.get(url, timeout=5)
      return html
    except requests.exceptions.RequestException:
      i += 1

def getAdministrativeDivision(code,level):
    url = "https://xingzhengquhua.51240.com/"+str(code)+"__xingzhengquhua/"
    url = url.strip()
    r = gethtml(url)
    #print(r.text)
    tree = etree.HTML(r.text)
    e=tree.xpath("//td[@bgcolor=\"#FFFFFF\"]/a")
    for i in range(6-level,len(e)):
        #print(etree.tostring(e[i]).decode('utf-8'))
        info = re.search(">.*</a>",etree.tostring(e[i]).decode('utf-8')).group()[1:][:-4]
        print(lxml.html.fromstring(info).text)
        name = lxml.html.fromstring(info).text
        #print(i)
        if i % 2 == level % 2:
            name_bkup = name
        else:
            code = name
            name = name_bkup
            sql = 'SELECT * FROM administrativeDivision WHERE code = '+str(code)
            cur.execute(sql)
            conn.commit()
            if not cur.fetchone():
                sql = ("INSERT INTO administrativeDivision VALUES (NULL ,'%s','%s','%s')")%(level,name,code)
                cur.execute(sql)
                conn.commit()
                print(sql)
            



conn = sqlite3.connect("./airbnbSpider.db")
cur=conn.cursor()

getAdministrativeDivision(310000000000,4)

for level in range(4,3,-1):
    sql = 'SELECT code FROM administrativeDivision WHERE level = '+str(level)
    #print(sql)
    cur_level=conn.cursor()
    cur_level.execute(sql)
    conn.commit()
    for row in cur_level:
        time.sleep(2)
        getAdministrativeDivision(row[0],level-1)


