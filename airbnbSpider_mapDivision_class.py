# -*- coding: UTF-8 -*-

import json
import re
import sqlite3
import pymysql
import threading
import time
import random
from threading import Semaphore, Thread

import chardet
import lxml
import requests
import scrapy
from lxml import etree
from requests.adapters import HTTPAdapter

class proxyPool:
    def __init__(self):
        self.proxyId = 0
        self.ip=""
        self.table = "`spideairbnb`.`proxypool`"
        self.db = pymysql.connect(
            "localhost", "root", "delta=b2-4ac", "spideairbnb")
        self.cursor = self.db.cursor()

    def dbInsert(self,proxy):
        sql = "INSERT INTO "+self.table+" (`ip`, `numused`, `state`) VALUES ('{}', '0', 'new')".format(proxy)
        self.cursor.execute(sql)
        self.db.commit()

    def IP(self):
        sql = "SELECT * from "+self.table+"WHERE `state` != 'del'"
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        if(len(results)<5):
            self.get()
            return self.IP()
        rand = random.randint(0,len(results)-1)
        #print(results[rand])
        self.ip = results[rand][1]
        self.proxyId = results[rand][0]
        return self.IP

    def proxies(self):
        self.IP()
        self.proxies = {
            "http": " http://{}".format(self.ip),
            "https": "https://{}".format(self.ip),
        }
        return self.proxies

    def get(self,num=5):
        url = "http://dps.kdlapi.com/api/getdps/?orderid=910553946536422&num={}&pt=1&format=json&sep=1".format(num)
        html = requests.get(url, timeout=5)
        #print(url)
        #print(html)
        res = json.loads(html.content)
        print("get proxy ",time.asctime(
                time.localtime(time.time())))
        if 'data' in res:
            res = res['data']
        else :
            print("get proxy err in data")
        count = res['count']

        if 'proxy_list' in res:
            proxys = res['proxy_list']
        else :
            print("get proxy err in proxy_list")

        for proxy in proxys :
            self.dbInsert(proxy)

    def delete(self):
        sql = "DELETE FROM "+self.table+" WHERE `id`='{}'".format(self.proxyId)
        self.cursor.execute(sql)
        self.db.commit()

class mapSpider:
    def __init__(self):
        self.lat_low = 0.0
        self.lat_upp = 0.0
        self.lon_low = 0.0
        self.lon_upp = 0.0
        self.id = 0
        self.num = -1
        self.db = pymysql.connect(
            "localhost", "root", "delta=b2-4ac", "spideairbnb")
        self.cursor = self.db.cursor()

        self.errInfo = ""
        self.url = ""
        self.json = ""
        self.html = ""
        self.table = "`spideairbnb`.`numofhousesavailable`"

    def __del__(self):
        self.db.close()

    def run(self):
        self.getTask()

    def dbUpdateStates(self, state):
        sql = "UPDATE "+self.table + \
            " SET `state`='{}' WHERE `id`='{}'".format(state, self.id)
        self.cursor.execute(sql)
        self.db.commit()

    def dbUpdateNum(self, num):
        sql = "UPDATE "+self.table + \
            " SET `num`='{}' WHERE `id`='{}'".format(num, self.id)
        self.cursor.execute(sql)
        self.db.commit()

    def dbInsert(self, location):
        sql = "INSERT INTO `spideairbnb`.`numofhousesavailable` \
            (`lat_low`, `lat_upp`, `lon_low`, `lon_upp`, `num`,`state`)\
            VALUES ('{}', '{}', '{}', '{}', '-1','todo')\
            ".format(location[0], location[1], location[2], location[3])
        self.cursor.execute(sql)
        print(sql)
        self.db.commit()

    def getTask(self):
        # 调取一条todo数据
        sql = "SELECT * FROM "+self.table+"  WHERE `state` = 'todo' OR `state` = 'processing' LIMIT 1 "
        print(sql)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if not len(results) == 1:
            self.errInfo = "have 0 todo entries."
            print(self.errInfo)
            return -1
        row = results[0]
        self.lat_low = row[1]
        self.lat_upp = row[2]
        self.lon_low = row[3]
        self.lon_upp = row[4]
        self.id = row[0]
        # 锁住该条数据
        self.dbUpdateStates("processing")
        self.fetch()

    def fetch(self):
        url = "https://www.airbnb.cn/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=true&client_session_id=d0c77d93-3a9a-43df-82fb-568ac0d5a566&currency=CNY&current_tab_id=home_tab&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=20&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=zh&metadata_only=false&query=%E4%B8%8A%E6%B5%B7&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&satori_config_token=EhIiQhIiIjISEjISIiIiUiUAIgA&satori_version=1.1.13&screen_height=425&screen_size=large&screen_width=1472&search_by_map=true&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=480&version=1.7.9&zoom=9"
        url += "&sw_lat={}".format(self.lat_low)
        url += "&sw_lng={}".format(self.lon_low)
        url += "&ne_lat={}".format(self.lat_upp)
        url += "&ne_lng={}".format(self.lon_upp)
        self.url = url
        #print(url)
        print(str(self.lat_low)+"----"+str(self.lat_upp)+"----"+str(self.lon_low)+"----"+str(self.lon_upp))
        self.gethtml()
        self.log()
        self.jsonDecode()

    def gethtml(self):
        url = self.url
        proxypool = proxyPool()
        proxies = proxypool.proxies()
        i = 0
        while i < 3:
            try:
                html = requests.get(url, timeout=5, proxies=proxies)
                #html = requests.get(url, timeout=5)
                if("429 Too Many Requests" in html.text):
                    print("429 error")
                    logFile = open('logFile.html', 'w', encoding='utf-8')
                    logFile.write(html.text)
                    logFile.close()
                self.json = json.loads(html.content)
                self.html = html              
                return
            except Exception as e:
                i += 1
                print("connect error and retry   :    "+str(e)[-70:])
                if 'Cannot connect to proxy' in str(e):
                    i = 6
        proxypool.delete()
        print("delete proxy : "+str(proxypool.ip))
        self.gethtml()

    def log(self):
        logFile = open('logFile.html', 'w', encoding='utf-8')
        while(self.json == None):
            print("None")
            self.gethtml()
        logFile.write(self.html.text)
        logFile.close()

    def jsonDecode(self):
        try:
            res = self.json
        except Exception:
            print(Exception, "getHTML", time.asctime(
                time.localtime(time.time())))
            return

        if 'home_tab_metadata' in res['explore_tabs'][0]:
            count = res['explore_tabs'][0]['home_tab_metadata']['listings_count']
            print(count)
            self.dbUpdateStates("done")
            self.dbUpdateNum(str(count))
            if(count > 50):
                self.quadrateDivision()

        else:
            print("房源总数未知")
            self.dbUpdateStates("todo")

    def quadrateDivision(self):
        self.lat_mid = (self.lat_low+self.lat_upp)/2
        self.lon_mid = (self.lon_low+self.lon_upp)/2
        locationList = []
        locationList.append((self.lat_low, self.lat_mid,
                             self.lon_low, self.lon_mid))
        locationList.append((self.lat_mid, self.lat_upp,
                             self.lon_low, self.lon_mid))
        locationList.append((self.lat_low, self.lat_mid,
                             self.lon_mid, self.lon_upp))
        locationList.append((self.lat_mid, self.lat_upp,
                             self.lon_mid, self.lon_upp))
        for location in locationList:
            self.dbInsert(location)

class listSpider(mapSpider):
    def __init__(self):
        super().__init__()
        self.mapTable = "`spideairbnb`.`numofhousesavailable`"
        self.listTable = "`spideairbnb`.`houselist`"
        self.offset = 0

    def __del__(self):
        self.db.close()

    def dbMapUpdateStates(self,state):
        sql =   "UPDATE "+self.mapTable + \
                " SET `state`='{}' WHERE `id`='{}'".format(state, self.id)
        self.cursor.execute(sql)
        self.db.commit()

    def dbHouseExist(self,house_id):
        sql =   "SELECT * FROM "+self.listTable + \
                "WHERE house_id = {}".format(house_id)
        self.cursor.execute(sql)
        self.db.commit()
        if(len(self.cursor.fetchall())>=1):
            return True
        else:
            return False

    def dbHouseInsert(self,price,description,house_id):
        sql = "INSERT INTO " + self.listTable + " VALUES (NULL ,'{}','{}','{}','{}')".format(
                                price, description, house_id,self.id)
        self.cursor.execute(sql)
        self.db.commit()

    def getTask(self):
        mapLock.acquire()

        sql = "SELECT * FROM "+self.mapTable+"  WHERE `state` = 'done' AND `num` < 50 AND `num` > 0"
        self.cursor.execute(sql)
        mapResults = self.cursor.fetchall()

        if len(mapResults) == 0:
            self.errInfo = "have 0 todo entries."
            print(self.errInfo)
            return -1
        
        mapRow = mapResults[0]
        self.lat_low = mapRow[1]
        self.lat_upp = mapRow[2]
        self.lon_low = mapRow[3]
        self.lon_upp = mapRow[4]
        self.id =      mapRow[0]
        self.dbMapUpdateStates("listing")
        mapLock.release()
        print("num:{}\t itemPerPage:{}\t numOfPages:{}  ".format(mapRow[5],40,int(mapRow[5]/20)))
        for self.page in range(int(mapRow[5]/40)+1):
            self.fetch(offset = self.page*40)
        
        print(self.id)

    def fetch(self,offset = 0):
        url = "https://www.airbnb.cn/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=true&client_session_id=d0c77d93-3a9a-43df-82fb-568ac0d5a566&currency=CNY&current_tab_id=home_tab&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=50&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=zh&metadata_only=false&query=%E4%B8%8A%E6%B5%B7&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&satori_config_token=EhIiQhIiIjISEjISIiIiUiUAIgA&satori_version=1.1.13&screen_height=425&screen_size=large&screen_width=1472&search_by_map=true&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=480&version=1.7.9&zoom=9"
        url += "&sw_lat={}".format(self.lat_low)
        url += "&sw_lng={}".format(self.lon_low)
        url += "&ne_lat={}".format(self.lat_upp)
        url += "&ne_lng={}".format(self.lon_upp)
        if not self.offset == 0:
            url += "&items_offset={}".format(self.offset)
        #print(url)
        self.url = url
        self.gethtml()
        self.log()
        self.jsonDecode()

    def jsonDecode(self): 
        try:
            res = self.json
        except Exception:
            print(Exception, "getHTML", time.asctime(
                time.localtime(time.time())))
            return

        if 'home_tab_metadata' in res['explore_tabs'][0]:
            count = res['explore_tabs'][0]['home_tab_metadata']['listings_count']
            sections = res['explore_tabs'][0]['sections']
            #print(self.url)
            #print(len(sections))
            for section in sections:
                self.exist = 0
                self.insert = 0
                #for key in section.keys():
                #    print(key)
                if 'listings' in section:
                    self.inDB = ""
                    listings = section['listings']
                    for listing in listings:
                        try:
                            self.decodeListing(listing)
                        except Exception as e:
                            print(str(e), "for listing", time.asctime(time.localtime(time.time())))
                    
                    print("{}   map_id:{}\tpage:{}\tcount;{}   共{}个，其中重复{}，新增{},{}".format(
                        threading.currentThread().getName(),self.id,self.page,count,str(len(listings)), self.exist, self.insert, self.inDB))
                    #print(threading.currentThread().getName())
        else:
            print("房源list解码异常")
            self.dbUpdateStates("done")

    def decodeListing(self,listing):
        price = listing['pricing_quote']['price_string']
        description = listing['listing']['name']
        house_id = listing['listing']['id']
        # print(house_id)
        description = description.replace("'", "''")
        description = description.replace('"', '""')
        if(self.dbHouseExist(house_id)):
            #self.dbHouseInsert(price,description,house_id)
            self.exist += 1
            self.inDB += "-"
        else:
            self.dbHouseInsert(price,description,house_id)
            self.insert += 1
            self.inDB += "&"

class calendarSpider(mapSpider):
    def __init__(self):
        super().__init__()
        self.mapTable = "`spideairbnb`.`numofhousesavailable`"
        self.listTable = "`spideairbnb`.`houselist`"
        self.calendartable = "`spiderairbnb`.`calendar`"
        self.offset = 0
        localtime = time.localtime(time.time())
        self.mouth = localtime[1]
        self.year = localtime[0]
        self.day = localtime[2]
        self.count = 3
        self.dtToday = "{}-{}-{}".format(self.year,self.mouth,self.day)

    def dateCompare(self,dt1,dt2):
        dt1 = time.mktime(time.strptime(dt1,'%Y-%m-%d'))
        dt2 = time.mktime(time.strptime(dt2,'%Y-%m-%d'))
        return dt1-dt2

    def fetch(self,house_id,map_id):
        self.house_id = house_id
        self.map_id = map_id
        url = "https://www.airbnb.cn/api/v2/homes_pdp_availability_calendar?currency=CNY&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=zh"
        url += "&listing_id={}".format(str(house_id))
        url += "&month={}".format(str(self.mouth))
        url += "&year={}".format(str(self.year))
        url += "&count={}".format(str(self.count))
        #print(url)
        self.url = url
        self.gethtml()
        self.log()
        self.jsonDecode()

    def jsonDecode(self):
        #print(self.html.text)
        try:
            res = self.json
        except Exception:
            print(Exception, "getHTML", time.asctime(
                time.localtime(time.time())))
            return

        dt1 = self.dtToday
        if 'metadata' in res:
            if not 'first_bookable_day' in res['metadata']:
                return
        if 'calendar_months' in res:
            for month in res['calendar_months']:
                for day in month['days']:
                    dt2 = day['date']
                    if( self.dateCompare(dt1,dt2) < 0 and day['available']==False ):
                        print(self.map_id,self.house_id,dt1,dt2)
                        self.dbInsert(day)

    def dbInsert(self,day):
        sql = "INSERT INTO `spideairbnb`.`calendar` (`house_id`, `map_id`, `fetch_date`, `reserved`) VALUES ('{}', '{}', '{}', '{}')".format(self.house_id,self.map_id,self.dtToday,day['date'])
        #print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        pass

def runListSpider():
    print(threading.currentThread().getName())
    spider = listSpider()
    spider.run()
    
def run_mapSpiser(): 
    sql = "SELECT * FROM `spideairbnb`.`numofhousesavailable` WHERE `state` = 'todo' OR `state` = 'processing' "
    db = pymysql.connect("localhost", "root", "delta=b2-4ac", "spideairbnb")
    cursor = db.cursor()
    while(1):
        spider = mapSpider()
        spider.run()
        sql = "SELECT * FROM `spideairbnb`.`numofhousesavailable` WHERE state = 'too' OR `state` = 'processing' "
        cursor.execute(sql)
        db.commit()
        results = cursor.fetchall()
        print(len(results))
        if len(results) == 0:
            break

    while(1):
        sm.acquire()
        time.sleep(0.2)
        th = threading.Thread(target=runListSpider,args=())
        th.start()
        sm.release()

def run_listSpider():
    db = pymysql.connect("localhost", "root", "delta=b2-4ac", "spideairbnb")
    cursor = db.cursor()

def runCalendarspider(house_id,map_id):
    calendar = calendarSpider()
    calendar.fetch(house_id,map_id)

def run_test_ip():
    pro = proxyPool()
    print(pro.IP())
    
def run_test_calendar():
    calendar = calendarSpider()

    db = pymysql.connect("localhost", "root", "delta=b2-4ac", "spideairbnb")
    cursor = db.cursor()
    sql = "SELECT * FROM spideairbnb.houselist"
    cursor.execute(sql)
    db.commit()
    results = cursor.fetchall()
    for row in results:
        sm.acquire()
        time.sleep(0.1)
        th = threading.Thread(target=runCalendarspider,args=(row[3],row[4]))
        th.start()
        sm.release()



mapLock = threading.Lock()
calendarLock = threading.Lock()
sm=threading.Semaphore(20)
if __name__ == "__main__":
    #run_mapSpiser()
    run_test_calendar()
