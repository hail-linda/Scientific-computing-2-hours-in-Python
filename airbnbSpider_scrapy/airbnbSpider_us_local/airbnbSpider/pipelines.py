# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from airbnbSpider.items import listItem,calendarItem,detailItem
import pymysql

from airbnbSpider import dbSettings
import time
import json, math
from threading import Semaphore, Thread
import threading,re

def filter_str(desstr, restr=''):
    # 过滤除中英文及数字以外的其他字符
    res = re.compile(u'[\U00010000-\U0010ffff\uD800-\uDBFF\uDC00-\uDFFF]')
    return res.sub(restr, desstr)


def dbCalendarInsert(house_id,response):
    calendarResponseTable = "`calendarresponse_us`"
    db = dbSettings.db_connect()
    cursor = db.cursor()
    sql = "INSERT INTO "+ calendarResponseTable+" (id, house_id, response) VALUES " \
                  "(NULL,'{}','{}')".format(house_id, response)
    cursor.execute(sql)
    db.commit()
    db.close()

def dbDetailInsert(house_id,response):
    # response = response.replace("'", "''").replace('"', '""')
    detailResponseTable = "`detailresponse`"
    db = dbSettings.db_connect()
    cursor = db.cursor()
    sql = "INSERT INTO "+ detailResponseTable+" (id, house_id, response) VALUES " \
                  "(NULL,%s,%s)"
    cursor.execute(sql,(house_id,response))
    db.commit()
    db.close()



class AirbnbspiderPipeline:

    def process_item(self, item, spider):

        self.table = "`proxypool_us`"
        self.db = dbSettings.db_connect()
        self.cursor = self.db.cursor()
        self.mapTable = "`map`"
        self.listTable = "`houselist_us`"
        self.mapresponseTable = "`mapresponse_us`"
        self.calendarResponseTable = "`calendarresponse_us`"

        if  item.__class__ == listItem:
            st = time.time()
            res = item['response'].replace("'", "''")
            res = res.replace('"', '""')
            sql = "INSERT INTO " + self.mapresponseTable + " VALUES (NULL ,'{}')".format(res)
            self.cursor.execute(sql)
            self.db.commit()
            # print("item time:"+str(int(1000*(time.time()-st)))+"ms")
            return

            res = json.loads(item['response'])
            if 'home_tab_metadata' in res['explore_tabs'][0]:
                count = res['explore_tabs'][0]['home_tab_metadata']['listings_count']
                sections = res['explore_tabs'][0]['sections']
                for section in sections:
                    self.exist = 0
                    self.insert = 0
                    if 'listings' in section:
                        self.inDB = ""
                        listings = section['listings']
                        for listing in listings:
                            try:
                                self.decodeListing(listing)
                            except Exception as e:
                                print(str(e), "for listing", time.asctime(
                                    time.localtime(time.time())))

                        print(" count;{}   共{}个，其中重复{}，新增{},{}".format(
                             count, str(len(listings)), self.exist, self.insert, self.inDB))
            else:
                print("房源list解码异常")
                self.dbUpdateStates("done")

        elif item.__class__ == calendarItem:
            dbCalendarInsert(item['house_id'], item['response'])
            # th = threading.Thread(target=dbCalendarInsert, args=(item['house_id'], item['response']))
            # th.start()
            print("house id: ",item['house_id'],"len of response: ",len(item['response']))
  
            # sql = "INSERT IGNORE INTO "+self.calendarResponseTable+" (id, house_id, response) VALUES " \
            #       "(NULL,'{}','{}')".format(item['house_id'], item['response'])
            # self.cursor.execute(sql)
            # self.db.commit()

        elif item.__class__ == detailItem:
            dbDetailInsert(item['house_id'], item['response'])
            print(item['house_id'])

        return item

    def dbMapUpdateStates(self, state):
        sql = "UPDATE "+self.mapTable + \
            " SET `state`='{}' WHERE `id`='{}'".format(state, self.id)
        self.cursor.execute(sql)
        self.db.commit()

    def dbHouseExist(self, house_id):
        sql = "SELECT * FROM "+self.listTable + \
            "WHERE house_id = {}".format(house_id)
        self.cursor.execute(sql)
        self.db.commit()
        if(len(self.cursor.fetchall()) >= 1):
            return True
        else:
            return False

    def dbHouseInsert(self, price, description, house_id):
        sql = "INSERT INTO " + self.listTable + " VALUES (NULL ,'{}','{}','{}','{}')".format(
            price, description, house_id,123)
        # print(sql)
        self.cursor.execute(sql)
        self.db.commit()

    def decodeListing(self, listing):
        price = listing['pricing_quote']['price_string']
        description = listing['listing']['name']
        house_id = listing['listing']['id']
        # print(house_id)
        description = description.replace("'", "''")
        description = description.replace('"', '""')
        if(self.dbHouseExist(house_id)):
            # self.dbHouseInsert(price,description,house_id)
            self.exist += 1
            self.inDB += "-"
        else:
            self.dbHouseInsert(price, description, house_id)
            self.insert += 1
            self.inDB += "&"
    

