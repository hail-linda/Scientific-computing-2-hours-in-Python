import json, math
from airbnbSpider.items import listItem
from airbnbSpider.items import calendarItem
from scrapy.spiders import Spider
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.utils import bytes_to_str

import base64
import pymysql
from airbnbSpider import dbSettings
import time
import json
import random

class proxyPool:
    def __init__(self):
        self.proxyId = 0
        self.ip = ""
        self.table = "`proxypool`"
        self.db = dbSettings.db_connect()
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
    errInfo = ""
    url = ""
    json = ""
    html = ""
    starttime=time.time()

    localtime = time.localtime(time.time())
    mouth = localtime[1]
    year = localtime[0]
    day = localtime[2]

    name = "calendar"
    allowed_domains = ['www.airbnb.cn']
    redis_key = 'calendar:start_urls'

    def __del__(self):
        pass

    def make_request_from_data(self, data):
        house_id = bytes_to_str(data, self.redis_encoding)
        meta = {'house_id': house_id,"handle_httpstatus_all": True}
        return Request(  url = self.urlJoint(house_id),callback = self.calendarParse,
                            errback=self.calendarErrback,meta = meta, dont_filter=True,
                             headers={('User-Agent', 'Mozilla/5.0')})

    def urlJoint(self, house_id):
        url = "https://www.airbnb.cn/api/v2/homes_pdp_availability_calendar?currency=CNY&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=zh"
        url += "&listing_id={}&month={}&year={}&count={}".format(str(house_id),str(self.mouth),str(self.year),"3")
        print(url)
        return url

    def calendarParse(self,response):
        item = calendarItem()
        item['house_id'] = response.meta['house_id']
        item['response'] = response.body.decode('utf8')
        yield item

    def calendarErrback(self,failure):
        # 假设我们需要对指定的异常类型做处理，
        # 我们需要判断异常的类型
        response = failure.value
        print("Errback repr:\t"+repr(response))
        print("Errback:\t"+str(response))
        print(failure.request.meta)
        print(failure.request.meta['proxy'][8:])

        print(failure)
        proxypool = proxyPool()
        proxypool.delete(failure.request.meta['proxy'][8:],str(response))
        print("del proxy:"+str(failure.request.meta['proxy'][8:]))
        del proxypool

        yield failure.request
