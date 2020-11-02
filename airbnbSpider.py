 # -*- coding: UTF-8 -*-

import sqlite3
import numpy as np
import requests,json,chardet
import time
from requests.adapters import HTTPAdapter
import threading
from threading import Thread, Semaphore
import scrapy,re
from lxml import etree
import lxml



def gethtml(url):
  
  proxies = {
  "http":" http://60.2.145.75:3128",
  "https":"https://60.2.145.75:3128",
  }
  i = 0
  while i < 3:
    try:
      html = requests.get(url, timeout=5,proxies=proxies)
      return html
    except requests.exceptions.RequestException:
      i += 1

def getAirbnb(locate,offset=0):

    url = "https://www.airbnb.cn/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=true&client_session_id=3ae72c67-94f2-4a32-a775-4f906ce7d13e&currency=CNY&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=50&has_zero_guest_treatment=true&hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=50&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=zh&map_toggle=true&metadata_only=false&query="+str(locate)
    url = url.strip()
    time.sleep(0.1)
    if not offset == 0:
      url += "&items_offset="+str(offset)

    r = gethtml(url)

      
    logFile = open('logFile.html', 'w',encoding='utf-8')  
    logFile.write(r.text)
    logFile.close()
    count = 300
    try:
      res = json.loads(r.content)
    except Exception:
      print(Exception,"getHTML",time.asctime( time.localtime(time.time()) ))
      print(count,offset)
      getAirbnb(locate,offset)
      if(count-offset>50):
        #ime.sleep(1)
        getAirbnb(locate,offset+50)
      return

 
    if 'home_tab_metadata' in res['explore_tabs'][0]:
      count = res['explore_tabs'][0]['home_tab_metadata']['listings_count']

    sections = res['explore_tabs'][0]['sections']
    conn_temp = sqlite3.connect("./airbnbSpider.db")
    cur_temp = conn_temp.cursor()
    for section in sections:
      exist = 0
      insert = 0
      if 'listings' in section:
        listings = section['listings']
        
        inDB=""

        for listing in listings:
          try:
            price = listing['pricing_quote']['price_string']
            description = listing['listing']['name']
            house_id = listing['listing']['id']
            #print(house_id)
            description= description.replace("'","''")
            description= description.replace('"','""')
            #print(price,description)
            sql = 'SELECT * FROM housing WHERE house_id = '+ str(house_id)
            #print(sql)
            cur_temp.execute(sql)
            conn_temp.commit()
            if not cur_temp.fetchone():
                sql = ("INSERT INTO housing VALUES (NULL ,'%s','%s','%s','%s')")%(locate,price,description,house_id)
                cur_temp.execute(sql)
                conn_temp.commit()
                #print("     -------INSERT-------")
                insert += 1
                inDB += "-"
            else:
              exist += 1
              inDB += "$"
          except Exception as e:
            print(str(e),"for listing",time.asctime( time.localtime(time.time()) ))
            getAirbnb(locate,offset)
            pass
        print("数量："+str(len(listings)),time.asctime( time.localtime(time.time()) ))
        print("共{}个，其中重复{}，新增{},{}".format(str(len(listings)),exist,insert,inDB))
    conn_temp.close()


    print(count,offset,locate)
    if(count-offset>50):
      ##time.sleep(1)
      getAirbnb(locate,offset+50)


def main():
  sem = threading.Semaphore(3)
  conn = sqlite3.connect("./airbnbSpider.db")
  cur=conn.cursor()
  flag = 1
  sql = 'SELECT * FROM administrativeDivision WHERE level = 3'
  cur_locate_3=conn.cursor()
  cur_locate_3.execute(sql)
  conn.commit()
  locates=[]
  for row3 in cur_locate_3:
    name = row3[2]
    code = row3[3]
    sql = 'SELECT * FROM administrativeDivision WHERE code = '+str(code)[:4]+"00000000"
    cur_locate_2 = conn.cursor()
    cur_locate_2.execute(sql)
    conn.commit()
    for row2 in cur_locate_2 :
      name = "上海市"+row2[2]+name
      name = name.replace("市辖区","")
      #print(name)
      if(flag == 1):
        locates.append(name)

  conn.close()

  locates.append("上海市")

  for locate in locates:

    getAirbnb(locate)
'''
    print(locate)
    sem.acquire()
    thread_run = threading.Thread(target=getAirbnb , args=(name,))
    thread_run.start()
    print("锁数量："+str(sem._value))
    sem.release()
'''


if __name__ == "__main__":
  main()




