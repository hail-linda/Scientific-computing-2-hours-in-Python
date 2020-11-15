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
        url = "http://dps.kdlapi.com/api/getdps/?orderid=910542824747856&num={}&pt=1&format=json&sep=1".format(num)
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
        self.lock = threading.RLock()

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
        self.lock.acquire()

        sql = "SELECT * FROM "+self.mapTable+"  WHERE (`state` = 'done' OR `state` = 'listing') AND `num` < 50 AND `num` > 0"
        self.cursor.execute(sql)
        mapResults = self.cursor.fetchall()

        if len(mapResults) == 0:
            self.errInfo = "have 0 todo entries."
            print(self.errInfo)
            return -1
        
        for mapRow in mapResults:
            sql = "SELECT * FROM {} WHERE `map_id` = {}\
                ".format(self.listTable,mapRow[0])
            self.cursor.execute(sql)
            listResult = self.cursor.fetchall()
            if len(listResult) == 0 or mapRow[5]-len(listResult) > 30 :
                self.lat_low = mapRow[1]
                self.lat_upp = mapRow[2]
                self.lon_low = mapRow[3]
                self.lon_upp = mapRow[4]
                self.id =      mapRow[0]
                self.dbMapUpdateStates("listing")
                print("num:{}\t itemPerPage:{}\t numOfPages:{}  ".format(mapRow[5],20,int(mapRow[5]/20)))
                for self.page in range(int(mapRow[5]/20)+1):
                    self.fetch(offset = self.page*20)
        self.lock.release()
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
                    
                    print("map_id:{}\tpage:{}\tcount;{}\t共{}个，其中重复{}，新增{},{}".format(
                        self.id,self.page,count,str(len(listings)), self.exist, self.insert, self.inDB))

        else:
            print("房源总数未知异常")
            self.dbUpdateStates("done")

    def decodeListing(self,listing):
        price = listing['pricing_quote']['price_string']
        description = listing['listing']['name']
        house_id = listing['listing']['id']
        # print(house_id)
        description = description.replace("'", "''")
        description = description.replace('"', '""')
        if(self.dbHouseExist(house_id)):
            self.dbHouseInsert(price,description,house_id)
            self.exist += 1
            self.inDB += "-"
        else:
            self.dbHouseInsert(price,description,house_id)
            self.insert += 1
            self.inDB += "&"


def getAirbnb(locate, offset=0, price_max=-1, price_min=-1):
    url = "https://www.airbnb.cn/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=true&client_session_id=8865391a-6117-4615-a0d3-b0cc83adc28a&currency=CNY&current_tab_id=home_tab&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=20&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=zh&map_toggle=true&metadata_only=false&place_id=ChIJMzz1sUBwsjURoWTDI5QSlQI&query_understanding_enabled=true&refinement_paths[]=%2Fhomes&satori_config_token=EhIiQhIiIjISEjISIiIiUgA&satori_version=1.1.13&screen_height=425&screen_size=large&screen_width=1472&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=480&version=1.7.9&query=" + \
        str(locate)

    url = url.strip()
    time.sleep(0.5)
    if not offset == 0:
        url += "&items_offset="+str(offset)

    if not price_max == -1 and not price_min == -1:
        url += "&price_max="+str(price_max)
        url += "&price_min="+str(price_min)
        print("价格区间："+str(price_min)+" -- "+str(price_max))

    # print(url)
    r = gethtml(url)

    logFile = open('logFile.html', 'w', encoding='utf-8')
    while(r == None):
        print("None")
        r = gethtml(url)
    logFile.write(r.text)
    logFile.close()
    count = 1000
    try:
        res = json.loads(r.content)
    except Exception:
        print(Exception, "getHTML", time.asctime(time.localtime(time.time())))
        print(count, offset)
        getAirbnb(locate, offset)
        if(count-offset > 50):
            # ime.sleep(1)
            getAirbnb(locate, offset+50)
        return

    if 'home_tab_metadata' in res['explore_tabs'][0]:
        count = res['explore_tabs'][0]['home_tab_metadata']['listings_count']
        if(count > 300):
            if(price_max == -1 or price_min == -1):
                print("房源数："+str(count)+"  min:0  max:5000")
                getAirbnb(locate, price_max=5000, price_min=0)
            else:
                print("房源数："+str(count)+"  min:" +
                      str(price_min)+"  max:"+str(price_max))
                midd = int(0.5*(price_max+price_min))
                getAirbnb(locate, price_max=midd, price_min=price_min)
                getAirbnb(locate, price_max=price_max, price_min=midd)

            return
    else:
        print("房源总数未知")

    sections = res['explore_tabs'][0]['sections']
    conn_temp = sqlite3.connect("./airbnbSpider.db")
    cur_temp = conn_temp.cursor()
    for section in sections:
        exist = 0
        insert = 0
        if 'listings' in section:
            listings = section['listings']

            inDB = ""
            for listing in listings:
                try:
                    price = listing['pricing_quote']['price_string']
                    description = listing['listing']['name']
                    house_id = listing['listing']['id']
                    # print(house_id)
                    description = description.replace("'", "''")
                    description = description.replace('"', '""')
                    # print(price,description)
                    sql = 'SELECT * FROM housing WHERE house_id = ' + \
                        str(house_id)
                    # print(sql)
                    cur_temp.execute(sql)
                    conn_temp.commit()
                    if not cur_temp.fetchone():
                        sql = ("INSERT INTO housing VALUES (NULL ,'%s','%s','%s','%s')") % (
                            locate, price, description, house_id)
                        cur_temp.execute(sql)
                        conn_temp.commit()
                        #print("     -------INSERT-------")
                        insert += 1
                        inDB += "-"
                    else:
                        exist += 1
                        inDB += "$"
                except Exception as e:
                    print(str(e), "for listing", time.asctime(
                        time.localtime(time.time())))
                    getAirbnb(locate, offset)
                    pass
            print("数量："+str(len(listings)),
                  time.asctime(time.localtime(time.time())))
            print("共{}个，其中重复{}，新增{},{}".format(
                str(len(listings)), exist, insert, inDB))
    conn_temp.close()

    print(count, offset, locate)
    if(count-offset > 50):
        # time.sleep(1)
        getAirbnb(locate, offset+50)

def runListSpider():
    print(threading.currentThread().getName())
    sm.acquire()
   
    spider = listSpider()
    spider.run()
    sm.release()


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
        time.sleep(1)
        th = threading.Thread(target=runListSpider,args=())
        th.start()

def run_listSpider():
    db = pymysql.connect("localhost", "root", "delta=b2-4ac", "spideairbnb")
    cursor = db.cursor()



def run_test():
    pro = proxyPool()
    print(pro.IP())


sm=threading.Semaphore(3)
if __name__ == "__main__":
    run_mapSpiser()
    #run_test()
