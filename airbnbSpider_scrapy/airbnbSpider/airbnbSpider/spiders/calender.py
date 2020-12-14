import json, math
from airbnbSpider.items import listItem
from airbnbSpider.items import CalenderItem
from scrapy.spiders import Spider
from scrapy import Request
from scrapy_redis.spiders import RedisSpider

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

class calenderSpider(RedisSpider):
    name = "calender"
    allowed_domains = ['www.airbnb.cn']
    redis_key = 'calendar:start_urls'

    def __init__(self):

        self.num = -1
        self.db = pymysql.connect(
            "localhost", "root", "delta=b2-4ac", "airbnbspider")
        self.cursor = self.db.cursor()

        self.errInfo = ""
        self.url = ""
        self.json = ""
        self.html = ""
        self.mapTable = "`airbnbspider`.`map`"
        self.listTable = "`airbnbspider`.`houselist`"
        self.calendartable = "`airbnbspider`.`calendar`"
        self.starttime=time.time()

        localtime = time.localtime(time.time())
        self.mouth = localtime[1]
        self.year = localtime[0]
        self.day = localtime[2]


    def __del__(self):
        self.db.close()

    def make_request_from_data(self, data):
        house_id = bytes_to_str(data, self.redis_encoding)
        meta = {'house_id': house_id}
        yield Request(  url = self.urlJoint(house_id),callback = self.calendarParse,
                            errback=self.calendarErrback,meta = meta, dont_filter=True)


    def urlJoint(self, house_id):
        url = "https://www.airbnb.cn/api/v2/homes_pdp_availability_calendar?currency=CNY&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=zh"
        url += "&listing_id={}".format(str(house_id))
        url += "&month={}".format(str(self.mouth))
        url += "&year={}".format(str(self.year))
        url += "&count={}".format(str(self.count))
        return url

    def calendarParse(self,response):
        item = CalendarItem()
        item['house_id'] = response.meta['house_id']
        item['response'] = response.body.decode('utf8')
        yield item

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