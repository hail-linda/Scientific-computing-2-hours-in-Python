import json, math
from airbnbSpider.items import listItem
from scrapy.spiders import Spider
from scrapy import Request

import base64
import pymysql
import time
import json
import random

class proxyPool:
    def __init__(self):
        self.proxyId = 0
        self.ip = ""
        self.table = "`airbnbspider`.`proxypool`"
        self.db = pymysql.connect(
            "localhost", "root", "delta=b2-4ac", "spideairbnb")
        self.cursor = self.db.cursor()

    def delete(self, proxy, delReason):
        delReason = delReason.replace("'", "''")
        delReason = delReason.replace('"', '""')
        sql = "UPDATE "+self.table + \
            " SET `state` = 'del' WHERE `ip`='{}'".format(proxy)
        self.cursor.execute(sql)
        self.db.commit()
        sql = "UPDATE "+self.table + \
            " SET `delreason` = '{}' WHERE `ip`='{}'".format(
                delReason, proxy)

        print(sql)
        self.cursor.execute(sql)
        self.db.commit()

class mapSpider(Spider):
    name = "map"
    allowed_domains = ['www.airbnb.cn']

    def __init__(self):
        self.lat_low = 0.0
        self.lat_upp = 0.0
        self.lon_low = 0.0
        self.lon_upp = 0.0
        self.id = 0
        self.num = -1
        self.db = pymysql.connect(
            "localhost", "root", "delta=b2-4ac", "airbnbspider")
        self.cursor = self.db.cursor()
        self.area = ""

        self.errInfo = ""
        self.url = ""
        self.json = ""
        self.html = ""
        self.table = "`airbnbspider`.`map`"
        self.starttime=time.time()


    def __del__(self):
        self.db.close()

    def start_requests(self): 
        sql = "SELECT * FROM "+self.table + \
                "  WHERE (`state` = 'todo' OR `state` = 'processing')" 
        # print(sql)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if(len(results)==0):
            return 

        for row in results:
            # print(row[1])
            self.lat_low = row[1]
            self.lat_upp = row[2]
            self.lon_low = row[3]
            self.lon_upp = row[4]
            self.area = row[7]
            self.id = row[0]
            # self.dbUpdateStates("processing",self.id)
            meta = {"location":[row[1],row[2],row[3],row[4]],"map_id":row[0],"area":row[7],"starttime":time.time()}
            yield Request(  url = self.urlJoint(row),callback = self.mapParse,
                            errback=self.mapErrback,meta = meta, dont_filter=True)

    def re_requests(self): 
        sql = "SELECT * FROM "+self.table + \
                "  WHERE (`state` = 'todo' OR `state` = 'processing') " 
        # print(sql)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if(len(results)==0):
            return 

        for row in results:
            # print(row[1])
            self.lat_low = row[1]
            self.lat_upp = row[2]
            self.lon_low = row[3]
            self.lon_upp = row[4]
            self.area = row[7]
            self.id = row[0]
            # self.dbUpdateStates("processing",self.id)
            meta = {"location":[row[1],row[2],row[3],row[4]],"map_id":row[0],"area":row[7]}
            yield Request(  url = self.urlJoint(row),callback = self.mapParse,
                            errback=self.mapErrback,meta = meta, dont_filter=True)
  
    def dbUpdateStates(self, state, id):
        sql = "UPDATE "+self.table + \
            " SET `state`='{}' WHERE `id`='{}'".format(state, id)
        self.cursor.execute(sql)
        self.db.commit()

    def dbUpdateNum(self, num, id):
        sql = "UPDATE "+self.table + \
            " SET `num`='{}' WHERE `id`='{}'".format(num, id)
        self.cursor.execute(sql)
        self.db.commit()

    def dbInsert(self, location,area):
        sql = "INSERT INTO "+self.table + \
            "(`lat_low`, `lat_upp`, `lon_low`, `lon_upp`, `num`,`state`,`area`)\
            VALUES ('{}', '{}', '{}', '{}', '-1','todo','{}')\
            ".format(location[0], location[1], location[2], location[3], area)
        self.cursor.execute(sql)
        # print(sql)
        self.db.commit()

    def urlJoint(self, row):
        url = "https://www.airbnb.cn/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=true&client_session_id=d0c77d93-3a9a-43df-82fb-568ac0d5a566&currency=CNY&current_tab_id=home_tab&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=50&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=zh&metadata_only=false&query=%E4%B8%8A%E6%B5%B7&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&satori_config_token=EhIiQhIiIjISEjISIiIiUiUAIgA&satori_version=1.1.13&screen_height=425&screen_size=large&screen_width=1472&search_by_map=true&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=480&version=1.7.9&zoom=9"
        url += "&sw_lat={}&sw_lng={}&ne_lat={}&ne_lng={}".format(row[1],row[3],row[2],row[4])
        # url += "&sw_lng={}".format(row[3])
        # url += "&ne_lat={}".format(row[2])
        # url += "&ne_lng={}".format(row[4])
        # print(url)
        # print(str(self)+"----"+str(row[0]))
        # print(str(self)+"----"+str(row[0])+"----"+str(row[1])+"----" +
        #       str(row[2])+"----"+str(row[3])+"----"+str(row[4]))
        return url

    def mapParse(self,response):
        

        # print("mapParse")
        res = json.loads(response.body.decode('utf8'))
        if 'home_tab_metadata' in res['explore_tabs'][0]:
            count = res['explore_tabs'][0]['home_tab_metadata']['listings_count']
            print("mapParse:\t\t"+str(count))
            if(count > 50):
                pass
                self.quadrateDivision(response.meta)
            if(count<=50):
                item = listItem()
                item['response']=response.body.decode('utf8')
                print(str(int(1000*(time.time()-self.starttime)))+"ms")
                self.starttime = time.time()
                yield item
            self.dbUpdateStates("done",response.meta["map_id"])
            self.dbUpdateNum(str(count),response.meta["map_id"])

    def mapErrback(self,failure):
        # 假设我们需要对指定的异常类型做处理，
        # 我们需要判断异常的类型

        response = failure.value
        print("Errback:\t"+str(response))
        print(failure.request.meta['proxy'][8:])

        proxypool = proxyPool()
        proxypool.delete(failure.request.meta['proxy'][8:],str(response))
        print("del proxy:"+str(failure.request.meta['proxy'][8:]))
        del proxypool

        yield failure.request

    def quadrateDivision(self,meta):
        lat_low = meta["location"][0]
        lat_upp = meta["location"][1]
        lon_low = meta["location"][2]
        lon_upp = meta["location"][3]
        lat_mid = (lat_low+lat_upp)/2
        lon_mid = (lon_low+lon_upp)/2
        locationList = []
        locationList.append((lat_low, lat_mid,
                             lon_low, lon_mid))
        locationList.append((lat_mid, lat_upp,
                             lon_low, lon_mid))
        locationList.append((lat_low, lat_mid,
                             lon_mid, lon_upp))
        locationList.append((lat_mid, lat_upp,
                             lon_mid, lon_upp))
        for location in locationList:
            self.dbInsert(location,meta["area"])
        print("Insert 4 map area")
        self.re_requests()
























