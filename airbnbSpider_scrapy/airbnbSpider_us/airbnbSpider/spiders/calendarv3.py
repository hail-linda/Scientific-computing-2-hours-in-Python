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
        self.table = "`proxypool_us`"
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

    name = "calendarv3"
    allowed_domains = ['www.airbnb.cn']
    redis_key = 'calendar_us:start_urls'

    def __del__(self):
        pass

    def make_request_from_data(self, data):
        house_id = bytes_to_str(data, self.redis_encoding)
        meta = {'house_id': house_id,'url':self.urlJoint(house_id),"handle_httpstatus_all": True}
        headers = {
            ('Host', 'www.airbnb.com'),
            ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'),
            ('X-Airbnb-GraphQL-Platform', 'web'),
            ('X-CSRF-Without-Token', '1'),
            ('X-Airbnb-GraphQL-Platform-Client','minimalist-niobe'),
            ('X-CSRF-Token','V4$.airbnb.com$opm5kBq-0g0$8lJYwSL1f0shxuWB0W0qspYwHd0v2xVVobVIanuD-AY='),
            ('X-Airbnb-API-Key','d306zoyjsyarp7ifhu67rjxn52tv0t20')


        }
        return Request(  url = self.urlJoint(house_id),callback = self.calendarParse,
                            errback=self.calendarErrback,meta = meta, dont_filter=True,
                             headers=headers)

    def urlJoint(self, house_id):
        # https://www.airbnb.com/api/v3/PdpAvailabilityCalendar?operationName=PdpAvailabilityCalendar&locale=en&currency=USDextensions={"persistedQuery":{"version":1,"sha256Hash":"dc360510dba53b5e2a32c7172d10cf31347d3c92263f40b38df331f0b363ec41"}}&_cb=1sm426g16se018
        url = 'https://www.airbnb.com/api/v3/PdpAvailabilityCalendar?operationName=PdpAvailabilityCalendar&locale=en&currency=USD&extensions={"persistedQuery":{"version":1,"sha256Hash":"dc360510dba53b5e2a32c7172d10cf31347d3c92263f40b38df331f0b363ec41"}}&_cb=1sm426g16se018'
        url += '&variables={"request":{"count":3,"listingId":"'+str(house_id)+'","month":'+str(self.mouth)+',"year":'+str(self.year)+'}}'
        print(url)
        return url

    def calendarParse(self,response):
        item = calendarItem()
        # print('\n',response.request.headers,'\n',response.request.url,'\n',response.request.cookies)
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
