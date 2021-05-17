import json, math
from airbnbSpider.items import listItem
from airbnbSpider.items import calendarItem
from airbnbSpider.items import detailItem
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

    name = "detail"
    allowed_domains = ['www.airbnb.cn']
    redis_key = 'detail:start_urls'

    def __del__(self):
        pass

    def make_request_from_data(self, data):
        house_id = bytes_to_str(data, self.redis_encoding)
        meta = {'house_id': house_id,"handle_httpstatus_all": True}
        headers = {
            ('User-Agent', 'Mozilla/5.0'),
            ('X-Airbnb-GraphQL-Platform-Client','apollo-niobe'),
            ('X-CSRF-Token','V4$.airbnb.cn$wPXtlwZHCOo$axPFMN6Y-FIzrRCv6IQQXLdHUIV6r9b9VWqFPO791kA='),
            ('X-Airbnb-API-Key','d306zoyjsyarp7ifhu67rjxn52tv0t20')
        }
        return Request(  url = self.urlJoint(house_id),callback = self.detailParse,
                            errback=self.detailErrback,meta = meta, dont_filter=True,
                             headers=headers)

    def urlJoint(self, house_id):
        url = "https://www.airbnb.cn/api/v3/StaysPdpSections?operationName=StaysPdpSections"
        url += "&locale=zh&currency=CNY&_cb=8ak49r1n6bkuj&variables="
        url += '{"id":"'
        url += str(base64.b64encode(bytes('StayListing:'+str(house_id),"utf-8")))[2:-1]
        url += '","pdpSectionsRequest":{"adults":"1","bypassTargetings":false,"causeId":null,"children":null,"disasterId":null,"discountedGuestFeeVersion":null,"displayExtensions":null,"federatedSearchId":null,"forceBoostPriorityMessageType":null,"infants":null,"interactionType":null,"invitationClaimed":false,"layouts":["SIDEBAR","SINGLE_COLUMN"],"pdpTypeOverride":null,"preview":false,"previousStateCheckIn":null,"previousStateCheckOut":null,"priceDropSource":null,"privateBooking":false,"promotionUuid":null,"searchId":null,"selectedCancellationPolicyId":null,"staysBookingMigrationEnabled":false,"translateUgc":false,"useNewSectionWrapperApi":false,"sectionIds":null,"checkIn":"2021-02-02","checkOut":"2021-02-03"}}'
        url += '&extensions={"persistedQuery":{"version":1,"sha256Hash":"dc360510dba53b5e2a32c7172d10cf31347d3c92263f40b38df331f0b363ec41"}}'
        # print(url)
        return url


    def detailParse(self,response):
        item = detailItem()
        item['house_id'] = response.meta['house_id']
        item['response'] = response.body.decode('utf8')
        yield item

    def detailErrback(self,failure):
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
