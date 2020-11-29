import requests, json
from log import get_logger
from scipy.stats import invgamma
import pandas as pd
import numpy as np
from task import Task
from settings import CITIES
from datetime import date, timedelta


class ListingTask(Task):
    url = "https://m.ctrip.com/restapi/soa2/16593/json/searchhouse?" \
          "_fxpcqlniredt=09031156211865914676&__gw_appid=99999999&__gw_ver" \
          "=1.0&__gw_from=600003546&__gw_platform=H5"
    def get_total_count(self, city_id, page_index, date_start, date_end, price_range, page_size=40):
        r = {"city_id": city_id, "page_index": page_index, "page_size": page_size, "response": "", "request": "",
             "code": 0,
             "current_price": None}
        payload = {
            "args": "{\"parameter\":{\"pageIndex\":" + str(page_index) + ",\"pageSize\":" + str(
                page_size) + ",\"onlyReturnTotalCount\":true,\"returnFilterConditions\":true,\"returnGeoConditions\":true,\"returnNavigations\":true,\"returnPriceHot\":true,\"conditions\":[{\"type\":1,\"gType\":0,\"value\":\"" + str(
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
        headers = {'content-type': 'application/json'}
        try:
            resp = requests.post(self.url, data=json.dumps(payload), headers=headers)

            resp_content = json.loads(resp.text)
            res = json.loads(resp_content['result'])
            total_count = res['data']['totalCount']
            r['total_count'] = total_count

            if total_count == 0 or total_count is None:
                return 0

        except Exception as e:
            self.logger.exception("Get listing total count error while creating listing task. " + str(e))
            return -1

        return total_count

    def gen_price_cutoffs(self, listings=10000, step=500, a=1.67, loc=-17.64, scale=546.13):
        """This function accepts the number of listings in a city, and return a list of integers as the cutoffs. 
        The default step (=500) will make sure that each interval contains about 500 results. 
        Start from the second element for the lowest intervel (0, cutoffs_list[1]).
        End with the last element and upper limit (cutoffs_list[-1], 100000) """
        rvs = invgamma.rvs(a, loc, scale, size=listings)
        sorted_prices = pd.Series(rvs).sort_values()
        cutoffs = sorted_prices.loc[[i for j, i in enumerate(sorted_prices.index) if j % step == 0]]
        cutoffs_list = np.array(np.floor(cutoffs), dtype='int').tolist()

        return cutoffs_list

    def get_cities(self):
        """
        Get cities from ctrip.com. Later we might get cities from database instead.
        :return: 
        """
        url = "https://m.ctrip.com/restapi/soa2/16593/json/getCityList?_fxpcqlniredt=09031157111978003970" \
              "&__gw_appid=99999999&__gw_ver=1.0&__gw_from=10320666865&__gw_platform=H5"
        headers = {'content-type': 'application/json'}
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

        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            _body = json.loads(response.text)
            cities = []
            _result = _body['result']
            result = json.loads(_result)
            data = result['data']
            _cities = data['cityGroup']['cities']
            for cities_letter_group in _cities.values():
                for city in cities_letter_group:
                    cities.append({'id': city['cityId'], 'name': city['cityName']})
            return cities
        except Exception as e:
            self.logger.exception(e)
            return None


    def run(self):
        max_price = 100000
        date_start = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        date_end = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")
        cities = self.get_cities()
        if cities is None:
            cities = CITIES

        for city in cities:
            total_count = self.get_total_count(city['id'], 0, date_start, date_end, "0," + str(max_price))

            if total_count == -1:
                self.logger.error("Total count is None while creating listing task. city_id: %s" % (city['id'],))
                # TODO: Send message by email
                continue
            if total_count < 1:
                self.logger.info("There is no house in city: %s" % (city['id'],))
                continue

            cut_offs = self.gen_price_cutoffs(total_count)
            cut_offs[0] = -1
            cut_offs.append(max_price)

            for i in range(len(cut_offs) - 1):
                price_range = str(cut_offs[i] + 1) + "," + str(cut_offs[i + 1])
                page_idx = 0
                # data = {"cid": city_id, "p": page_idx, "ds": date_start, "de": date_end, "pr": price_range}

                """page_idx, date_start and date_end are not required. 
                To save redis storage, we only store required parameters."""
                # data = "%s,%s,%s,%s,%s" % (city_id, price_range, page_idx, date_start, date_end)
                data = "%s|%s" % (city['id'], price_range)
                try:
                    self.redis.lpush("listing:start_urls", data)
                except Exception as e:
                    self.logger.exception(e)
                    # TODO: send message


if __name__ == "__main__":
    task = ListingTask()
    task.run()


    