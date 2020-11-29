import json, math
from scrapy.spiders import Spider
from scrapy import Request


class CitySpider(Spider):
    name = 'city'
    allowed_domains = ['m.ctrip.com']
    redis_key = 'city:start_urls'
    url = "https://m.ctrip.com/restapi/soa2/16593/json/getCityList?_fxpcqlniredt=09031157111978003970" \
          "&__gw_appid=99999999&__gw_ver=1.0&__gw_from=10320666865&__gw_platform=H5"
    headers = {'content-type': 'application/json'}

    def get_payload(self):
        payload = {
            "args": "{\"parameter\":{\"version\":\"1\"}}",
             "head": {"cid": "09031157111978003970", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888",
                      "syscode": "09", "auth": None,
                      "extension": [
                          {"name": "terminaltype", "value": "20"},
                            {"name": "devicetype", "value": "Macintosh"},
                            {"name": "devicebrand", "value": "undefined"},
                            {"name": "devicephone", "value": "Mac"},
                            {"name": "browsername", "value": "Safari"},
                            {"name": "browserver", "value": "605.1.15"},
                            {"name": "os", "value": "IOS"},
                            {"name": "osver", "value": "10.146"},
                            {"name": "channelid", "value": "2"},
                            {"name": "page", "value": "10320666865"},
                            {"name": "refpage", "value": ""},
                            {"name": "currentpage",
                            "value": "feb85487-ea6f-811d-20ae-1731ec2d34dc"},
                            {"name": "pagename", "value": "citylist"},
                            {"name": "refpagename", "value": ""},
                            {"name": "refpageid", "value": ""},
                            {"name": "vid", "value": ""},
                            {"name": "la", "value": ""},
                            {"name": "lo", "value": ""},
                            {"name": "geoType", "value": ""}, {"name": "traceid",
                                                              "value": "899371e7-ea7d-7c28-35dd-f263725e8d8b"},
                            {"name": "protocal", "value": "https"}]},
             "contentType": "json"
            }

        return payload


    def start_requests(self):
        payload = json.dumps(self.get_payload())
        yield Request(self.url, self.parse, method="POST", body=payload,
                             headers=self.headers, dont_filter=True)

    def parse(self, response):
        body = response.body.decode('utf8')
        _body = json.loads(body)
        cities = []
        try:
            _result = _body['result']
            result = json.loads(_result)
            data = result['data']
            _cities = data['cityGroup']['cities']
            for cities_letter_group in _cities.values():
                for city in cities_letter_group:
                    cities.append({'id': city['cityId'], 'name': city['cityName']})
            cities_js = json.dumps(cities)
            a = cities_js
        except Exception as e:
            self.logger.exception(e)

