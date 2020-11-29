import json
from ctrip.items import CalendarItem
from scrapy_redis.utils import bytes_to_str
from ctrip.spiders.base_spider import BaseSpider
from scrapy import Request


class CalendarSpider(BaseSpider):
    name = 'calendar'
    allowed_domains = ['m.ctrip.com']
    redis_key = 'calendar:start_urls'
    url = "https://m.ctrip.com/restapi/soa2/16593/gethousecalendar?" \
          "_fxpcqlniredt=09031156211865914676&__gw_appid=99999999&__gw_ver=1.0&" \
          "__gw_from=600003547&__gw_platform=H5"
    headers = {'content-type': 'application/json'}

    def get_payload(self, house_id):
        payload = {
            "args": "{\"parameter\":{\"unitId\":" + house_id + "}}",
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
                                   {"name": "traceid", "value": "77264bb8-2599-31c7-5930-c1d93a262fa1"},
                                   {"name": "protocal", "value": "https"}]}, "contentType": "json"
        }

        return payload



    def make_request_from_data(self, data):
        """Overrides make_request_from_data of RedisSpider, and then we could push post request parameters to Redis. 
        :param data: 
        :return: 
        """
        house_id = bytes_to_str(data, self.redis_encoding)

        payload = json.dumps(self.get_payload(house_id))
        meta = {'house_id': house_id}
        return Request(url=self.url, method="POST", callback=self.parse, meta=meta,
                       body=payload, headers=self.headers, dont_filter=True, errback=self.errback)


    def parse(self, response):
        item = CalendarItem()
        item['house_id'] = response.meta['house_id']
        item['response'] = response.body.decode('utf8')
        item['status'] = 0
        yield item


    def errback(self, failure):
        self.logger.error(repr(failure))
        item = CalendarItem()
        item['house_id'] = failure.response.meta['house_id']
        item['response'] = failure.response.body.decode('utf8')
        item['status'] = 2
        yield item