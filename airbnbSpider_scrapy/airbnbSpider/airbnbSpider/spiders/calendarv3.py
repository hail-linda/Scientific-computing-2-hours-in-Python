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
import json, re
import random
import logging
from scrapy.utils.project import get_project_settings

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

    name = "calendarv3"
    allowed_domains = ['www.airbnb.cn']
    redis_key = 'calendar:start_urls'

    def __del__(self):
        pass

    def make_request_from_data(self, data):
        # print("start make request: ",time.time())
        localtime = time.localtime(time.time())
        self.mouth = localtime[1]
        self.year = localtime[0]
        self.day = localtime[2]
        house_id = bytes_to_str(data, self.redis_encoding)
        url = self.urlJoint(house_id)
        meta = {'house_id': house_id,'url':url,"handle_httpstatus_all": True}
        headers = {
            # ('Host', 'www.airbnb.cn'),
            # ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'),
            # ('X-Airbnb-Supports-Airlock-V2','true'),
            # ('X-Airbnb-GraphQL-Platform-Client','apollo-niobe'),
            # ('Accept-Languaget','zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'),
            # ('Accept','*/*'),
            ('X-Airbnb-API-Key','d306zoyjsyarp7ifhu67rjxn52tv0t20')
        }
        # print("end make request: ",time.time())

        # settings = get_project_settings()
        # print ("Your CONCURRENT_REQUESTS is:\n%s" % (settings.get('CONCURRENT_REQUESTS')))
        return  Request(      url = url,callback = self.calendarParse,
                            errback=self.calendarErrback,meta = meta, dont_filter=True,
                             headers=headers)

    def urlJoint(self, house_id):
        url = 'https://www.airbnb.cn/api/v3/PdpAvailabilityCalendar?operationName=PdpAvailabilityCalendar&locale=zh&currency=CNY&_cb=1k8iij1dsnj90&extensions={"persistedQuery":{"version":1,"sha256Hash":"dc360510dba53b5e2a32c7172d10cf31347d3c92263f40b38df331f0b363ec41"}}'
        url += '&variables={"request":{"count":3,"listingId":"'+str(house_id)+'","month":'+str(self.mouth)+',"year":'+str(self.year)+'}}'
        print("start:  ",house_id)
        print(url)
        return url

    def calendarParse(self,response):
        item = calendarItem()
        # print("response['meta']:\t",response.meta)
        item['house_id'] = response.meta['house_id']
        item['response'] = response.body.decode('utf8')
        if len(item['response']) == 17221 and "arg2" in response.meta :
            print("********************")
        if len(item['response']) == 17221:
            headers = {
            ('X-Airbnb-API-Key','d306zoyjsyarp7ifhu67rjxn52tv0t20')
            }
            arg1 = re.search("arg1='([^']+)'", item['response']).group(1)
            # print(arg1)
            _0x23a392 = unsbox(arg1)
            arg2 = 'acw_sc__v2=' + hexXor(_0x23a392) + ";"
            meta = {'house_id': response.meta['house_id'],'url':response.meta['url'],"handle_httpstatus_all": True,"arg2":arg2,"last_proxy":response.meta['proxy']}
            # print("errMeta:",meta,response.meta)
            yield  Request(url =response.meta['url'],callback = self.calendarParse,
                            errback=self.calendarErrback,meta = meta, dont_filter=True,
                             headers=headers)
        
        # with open("/{}.html".format(response.meta['house_id']),"w") as f :
        #     f.write(response.body.decode('utf8'))
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


def unsbox(arg1):
    box = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19, 0xd, 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c, 0x22, 0x25, 0xc, 0x24]
    res = list(range(0, len(arg1)))
    for i in range(0, len(arg1)):
        j = arg1[i]
        for k in range(0, 40):
            if box[k] == i+1:
                res[k] = j
    res = "".join(res)
    return res

def hexXor(arg2):
    box = "3000176000856006061501533003690027800375"
    res = ""
    for i in range(0, 40, 2):
        arg_H = int(arg2[i:i+2], 16)
        box_H = int(box[i:i+2], 16)
        res += hex(arg_H ^ box_H)[2:].zfill(2)
    # print(res)
    return res