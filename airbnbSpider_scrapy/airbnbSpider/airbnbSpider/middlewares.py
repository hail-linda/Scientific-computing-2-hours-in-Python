# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import pymysql

from . import dbSettings
import time
import random
import logging
from w3lib.http import basic_auth_header

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

class proxyPool:
    def __init__(self):
        self.proxyId = 0
        self.ip = ""
        self.table = "`proxypool`"
        # print("middleline-proxyPool1")
        self.db = dbSettings.db_connect()
        # print("middline-proxyPool2")
        self.cursor = self.db.cursor()

    def dbInsert(self, proxy):
        sql = "INSERT INTO "+self.table + \
            " (`ip`, `numused`, `state`) VALUES ('{}', '0', 'new')".format(proxy)
        self.cursor.execute(sql)
        self.db.commit()

    def IP(self):
        sql = "SELECT id,ip,cookies from "+self.table+"WHERE `state` != 'del' limit 30"
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        if(len(results) < 5):
            pass
            time.sleep(2)
            return self.IP()
        rand = random.randint(0, len(results)-1)
        print(results[rand]['id'],results[rand]['ip'])
        self.ip = results[rand]['ip']

        self.cookies = results[rand]['cookies']
        print("results[rand]['cookies']:\t",results[rand]['cookies'])
        # print("self.ip",self.ip)
        self.proxyId = results[rand]['id']
        print(" results[rand]['id']:\t", results[rand]['id'])
        # print("\tip end\t: ",time.time())

        # sql = "UPDATE "+self.table + \
        #     " SET `numused` = `numused` + 1 WHERE `id` = " + \
        #     str(results[rand]['id'])
        # self.cursor.execute(sql)
        # self.db.commit()

        return self.IP

    def proxies(self):
        self.IP()
        # print("proxy ip:\t\t\t",self.ip)
        self.proxies = " http://{}".format(self.ip)
        return self.proxies
    
    def getCookies(self):
        return self.cookies


    def get(self, num=20):
        url = "http://dps.kdlapi.com/api/getdps/?orderid=970736318449376&num={}&pt=1&format=json&sep=1&dedup=1".format(
            str(num))
        print(url)
        proxies = {"http": None, "https": None}
        html = requests.get(url, timeout=5, proxies=proxies)

        # print(html)
        res = json.loads(html.content)
        print("get proxy ", time.asctime(
            time.localtime(time.time())))
        if 'data' in res:
            res = res['data']
        else:
            print("get proxy err in data")
        count = res['count']

        if 'proxy_list' in res:
            proxys = res['proxy_list']
        else:
            print("get proxy err in proxy_list")

        for proxy in proxys:
            self.dbInsert(proxy)

    def delete(self, delReason):
        sql = "UPDATE "+self.table + \
            " SET `state` = 'del' WHERE `id`='{}'".format(self.proxyId)
        self.cursor.execute(sql)
        self.db.commit()
        sql = "UPDATE "+self.table + \
            " SET `delreason` = '{}' WHERE `id`='{}'".format(
                delReason, self.proxyId)
        self.cursor.execute(sql)
        self.db.commit()


class proxyMiddleware:

    def __init__(self):
        
        self.user_agent_list = [
            'MSIE (MSIE 6.0; X11; Linux; i686) Opera 7.23',
            'Opera/9.20 (Macintosh; Intel Mac OS X; U; en)',
            'Opera/9.0 (Macintosh; PPC Mac OS X; U; en)',
            'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
            'Mozilla/4.76 [en_jp] (X11; U; SunOS 5.8 sun4u)',
            'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0',
            'Mozilla/4.77 [en] (X11; I; IRIX;64 6.5 IP30)',
            'Mozilla/4.8 [en] (X11; U; SunOS; 5.7 sun4u)'
        ]

    def process_request(self,request,spider):
        self.proxypool = proxyPool()
        # print("\tstart make proxy: ",time.time())
        proxies = self.proxypool.proxies()
        # print("\tproxies: ",time.time())
        # print("proxy: ",proxies)
        request.meta['proxy'] = proxies
        request.headers['Proxy-Authorization'] = "Basic MTI4MjI1NTQwNDoxMjM0NTY="
        # print("request.headers:\t",request.headers)
        # request.headers['USER_AGENT']=random.choice(self.user_agent_list)
        # print("\tcookies: ",time.time())
        # print("self.proxypool.getCookies():\t",self.proxypool.getCookies())
        request.headers['Cookies'] = self.proxypool.getCookies() 
        # request.headers['Cookies'] ="acw_sc__v2=60a26bd0387363bd7ba2b6b6514d856eb3445cd7; "
        print("request.headers['Cookies'123]",request.headers['Cookies'])
        # print("request.headers:\t",request.headers)
        print("request.meta:\t",request.meta)
        if "arg2" in request.meta:
            print("proxyCompare:\t",request.meta['proxy'],request.meta['last_proxy'])
            request.meta['proxy'] = request.meta['last_proxy']
            print("proxyCompare:\t",request.meta['proxy'],request.meta['last_proxy'])
            print("arg2:\t", request.meta['arg2'])
            request.headers['Cookies'] = 'acw_sc__v2=' +request.meta['arg2'][11:-1] + ";"
            print("request.headers['Cookies'456]",request.headers['Cookies'])
        # print("\tend make proxy: ",time.time())
        # print("using ip:"+str(proxies))
        # del proxypool



class AirbnbspiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AirbnbspiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
