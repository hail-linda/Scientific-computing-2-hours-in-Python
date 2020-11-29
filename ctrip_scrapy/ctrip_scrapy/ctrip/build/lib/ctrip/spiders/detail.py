import scrapy
from ctrip.db import db_connect
import json
from ctrip.items import HouseDetailItem
from scrapy_redis.spiders import RedisSpider


class DetialSpider(RedisSpider):
    name = 'detail'
    allowed_domains = ['m.ctrip.com']
    # start_urls = []

    def get_payload(self, house_id):
        payload = {
            "args": "{\"parameter\":{\"unitID\":" + house_id + "},\"abTests\":{\"200203_HTL_newvj\":{\"s\":true,\"v\":\"B\"}}}",
            "head": {"cid": "09031156211865914676", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888",
                     "syscode": "09", "auth": None,
                     "extension": [{"name": "allianceSid", "value": "1693366"},
                                   {"name": "allianceId", "value": "66672"},
                                   {"name": "awakeUnion",
                                    "value": "{\"OUID\":\"\",\"AllianceID\":\"66672\",\"SID\":\"1693366\",\"SourceID\":\"\",\"AppID\":\"\",\"OpenID\":\"\"}"},
                                   {"name": "terminaltype", "value": "20"},
                                   {"name": "devicetype", "value": "Macintosh"},
                                   {"name": "devicebrand", "value": "undefined"},
                                   {"name": "devicephone", "value": "Mac"},
                                   {"name": "browsername", "value": "Chrome"},
                                   {"name": "browserver", "value": "83.0.4103.116"}, {"name": "os", "value": "IOS"},
                                   {"name": "osver", "value": "10.146"}, {"name": "channelid", "value": "2"},
                                   {"name": "page", "value": "600003547"},
                                   {"name": "refpage", "value": "11b38ae1-c072-c462-7f17-5777d7ec22be"},
                                   {"name": "currentpage", "value": "f66842b8-b583-3059-e24b-0629b5c1e067"},
                                   {"name": "pagename", "value": "detail"}, {"name": "refpagename", "value": "newlist"},
                                   {"name": "refpageid", "value": "600003546"},
                                   {"name": "vid", "value": "1528867582551.2gnoif"}, {"name": "la", "value": ""},
                                   {"name": "lo", "value": ""}, {"name": "geoType", "value": ""},
                                   {"name": "traceid", "value": "ff533d3c-b61f-0ccf-7269-74c134c5a888"},
                                   {"name": "protocal", "value": "https"}]}, "contentType": "json"
        }

        return payload

    def get_houses(self):
        db, cursor = db_connect()
        sql = "SELECT hp.house_id, hdr.create_time FROM houses hp LEFT JOIN house_detail_response hdr " \
              "ON hp.house_id=hdr.house_id WHERE hdr.create_time IS NULL LIMIT 10"
        cursor.execute(sql)
        rows = cursor.fetchall()
        print(">>>>>>>>>" + str(len(rows)))
        return rows

    def start_requests(self):
        rows = self.get_houses()
        for row in rows:
            print("getting house id: %s" % (row['house_id'],))
            url = "https://m.ctrip.com/restapi/soa2/16593/getHouse?_fxpcqlniredt=09031156211865914676&__gw_appid=99999999&__gw_ver=1.0&__gw_from=600003547&__gw_platform=H5"
            headers = {'content-type': 'application/json'}
            payload = json.dumps(self.get_payload(row['house_id']))
            meta = {'house_id': row['house_id'], 'request': payload}

            yield scrapy.Request(url, self.parse, method="POST", body=payload,
                                 headers=headers, meta=meta)

    def parse(self, response):
        if response.status == 200:
            item = HouseDetailItem()
            item['house_id'] = response.meta['house_id']
            item['response'] = response.body.decode('utf8')
            item['request'] = response.meta['request']
            item['status'] = 0
            yield item

