import json, math
from ctrip.items import ListingItem
from scrapy_redis.utils import bytes_to_str
from ctrip.spiders.base_spider import BaseSpider
from scrapy import Request
from datetime import date, timedelta


class ListingSpider(BaseSpider):
    name = 'listing'
    allowed_domains = ['m.ctrip.com']
    redis_key = 'listing:start_urls'
    url = "https://m.ctrip.com/restapi/soa2/16593/json/searchhouse?" \
          "_fxpcqlniredt=09031156211865914676&__gw_appid=99999999&__gw_ver=1.0&" \
          "__gw_from=600003546&__gw_platform=H5"
    headers = {'content-type': 'application/json'}
    date_start = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    date_end = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")
    page_size = 40


    def get_payload(self, city_id, price_range, page_index, date_start, date_end, page_size = 40):
        payload = {
            "args": "{\"parameter\":{\"pageIndex\":" + str(page_index) + ",\"pageSize\":" + str(
                page_size) + ",\"onlyReturnTotalCount\":false,\"returnFilterConditions\":true,\"returnGeoConditions\":true,\"returnNavigations\":true,\"returnPriceHot\":true,\"conditions\":[{\"type\":1,\"gType\":0,\"value\":\"" + str(
                city_id) + "\"},{\"type\":2,\"gType\":0,\"value\":\"" + date_start + "\"},{\"type\":3,\"gType\":0,\"value\":\"" + date_end + "\"},{\"type\":7,\"gType\":3,\"value\":\"" + price_range + "\"},{\"type\":4,\"gType\":4,\"value\":\"2\"}],\"defaultKeyword\":\"\"},\"abTests\":{\"200203_HTL_newvj\":{\"s\":true,\"v\":\"B\"}}}",
            "head": {"cid": "09031156211865914676", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888",
                     "syscode": "09",
                     "auth": None,
                     "extension": [
                         {"name": "allianceSid", "value": "1693366"},
                         {"name": "allianceId", "value": "66672"},
                         {"name": "awakeUnion",
                          "value": "{\"OUID\":\"\",\"AllianceID\":\"66672\",\"SID\":\"1693366\",\"SourceID\":\"\",\"AppID\":\"\",\"OpenID\":\"\"}"},
                         {"name": "terminaltype", "value": "20"},
                         {"name": "devicetype", "value": "Macintosh"},
                         {"name": "devicebrand", "value": "undefined"},
                         {"name": "devicephone", "value": "Mac"},
                         {"name": "browsername", "value": "Chrome"},
                         {"name": "browserver", "value": "83.0.4103.116"},
                         {"name": "os", "value": "IOS"},
                         {"name": "osver", "value": "10.146"},
                         {"name": "channelid", "value": "2"},
                         {"name": "page", "value": "600003546"},
                         {"name": "refpage", "value": "b6df0d4c-6e51-a235-06cc-53834958dae5"},
                         {"name": "currentpage", "value": "fdd6c6bd-6bbd-f434-eda2-30e1abedd3a5"},
                         {"name": "pagename", "value": "newlist"},
                         {"name": "refpagename", "value": "newlist"},
                         {"name": "refpageid", "value": "600003546"},
                         {"name": "vid", "value": "1528867582551.2gnoif"},
                         {"name": "la", "value": ""},
                         {"name": "lo", "value": ""},
                         {"name": "geoType", "value": ""},
                         {"name": "traceid", "value": "4150367a-7ea2-e26f-078f-f7f130b7de25"},
                         {"name": "apiv", "value": "1"},
                         {"name": "protocal", "value": "https"}
                     ]},
            "contentType": "json"}

        return payload


    def make_request_from_data(self, data):
        """Overrides make_request_from_data of RedisSpider, and then we could push post request parameters to Redis. 
        :param data: string of "city_id|price_range"
        :return: 
        """
        data = bytes_to_str(data, self.redis_encoding)
        data = data.split("|")
        if len(data) < 1:
            self.logger.error("Data for listing has less than 2 params")
            return None

        city_id = data[0]
        price_range = data[1]
        page_index = 0

        payload = json.dumps(self.get_payload(city_id, price_range, page_index,
                                              self.date_start, self.date_end, self.page_size))

        meta = {"city_id": data[0], "price_range": data[1], "date_start": self.date_start,
                "date_end": self.date_end, "page_size": self.page_size, "page_index": page_index}

        self.logger.info("Start a first-page request for city_id:%s, price_range:%s" % (city_id, price_range))
        return Request(url=self.url, method="POST", callback=self.first_page_parse, meta=meta,
                       body=payload, headers=self.headers, dont_filter=True, errback=self.first_page_errback)


    def first_page_parse(self, response):
        item = ListingItem()
        for k in ["city_id", "price_range", "page_index", "page_size"]:
            item[k] = response.meta[k]

        item['response'] = response.body.decode('utf8')
        item['status'] = 0
        yield item

        resp_content = json.loads(item['response'])
        res = json.loads(resp_content['result'])
        total_count = res['data']['totalCount']

        if total_count:
            page_end = math.ceil(total_count / self.page_size) - 1

            city_id = response.meta['city_id']
            price_range = response.meta['price_range']


            for page_idx in range(1, page_end + 1):
                payload = json.dumps(self.get_payload(city_id, price_range, page_idx,
                                                  self.date_start, self.date_end, self.page_size))
                meta = {"city_id": city_id, "price_range": price_range, "date_start": self.date_start,
                        "date_end": self.date_end, "page_size": self.page_size, "page_index": page_idx}

                self.logger.info("Yield a request for city_id:%s, price_range:%s, page_index:%s" %
                                 (city_id, price_range, page_idx))
                yield Request(url=self.url, method="POST", callback=self.page_parse, meta=meta,
                           body=payload, headers=self.headers, dont_filter=True, errback=self.page_errback)


    def page_parse(self, response):
        item = ListingItem()
        for k in ["city_id", "price_range", "page_index", "page_size"]:
            item[k] = response.meta[k]

        item['response'] = response.body.decode('utf8')
        item['status'] = 0
        yield item


    def first_page_errback(self, failure):
        self.logger.error(repr(failure))
        item = ListingItem()
        for k in ["city_id", "price_range", "page_index", "page_size"]:
            item[k] = failure.response.meta[k]

        item['response'] = failure.response.body.decode('utf8')
        item['status'] = 2
        yield item


    def page_errback(self, failure):
        self.first_page_errback(failure)