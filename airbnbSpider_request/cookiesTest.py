# -*- coding: UTF-8 -*-

import json
import random
import re
import sqlite3
import threading
import time
from threading import Semaphore, Thread

import chardet
import lxml

import requests
import scrapy
from lxml import etree
from requests.adapters import HTTPAdapter

def getCookies(url,srcCookies=""):
    headers = {
        "cookies" : srcCookies
    }
    res = requests.get(url,headers = headers)
    # print(res.cookies)
    rootCookies = srcCookies
    for k, v in res.cookies.items():
        print(k + "=" + v)
        print()
        rootCookies += str(k)+"="+str(v)+";"
    return rootCookies

def getJson(url,cookies):
    headers = {
        # 'Host': 'www.airbnb.cn',
        # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        # 'Accept':'*/*',
        # 'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        # 'Accept-Encoding':'gzip, deflate, br',
        # 'Referer':'https://www.airbnb.cn/rooms/38253408?check_in=2021-01-24&check_out=2021-01-25&translate_ugc=false&source_impression_id=p3_1611506749_hfHoTSSZpE2SS1ju',
        # 'content-type':'application/json',
        # 'X-Airbnb-GraphQL-Platform':'web',
        'X-Airbnb-GraphQL-Platform-Client':'apollo-niobe',
        'X-CSRF-Token':'V4$.airbnb.cn$0X3DthdMriM$xRMIhHuXGfgPZnD1CnDlEcI2HTkVfhQ1_NS_1bLacmM=',
        'X-Airbnb-API-Key':'d306zoyjsyarp7ifhu67rjxn52tv0t20',
        # 'X-CSRF-Without-Token':'1',
        # 'Connection':'keep-alive',
        'Cookie':pgPixelCookies,
        # 'Pragma':'no-cache',
        # 'Cache-Control':'no-cache',
        # 'TE':'Trailers',
    }
    res = requests.get(url,headers = headers)
    # res = json.loads(res, strict=False)
    print(res)
    print(res.content)


if __name__ == "__main__":

    rootCookies = getCookies("https://www.airbnb.cn")
    # print(rootCookies)
    print()
    pgPixelCookies = getCookies("https://www.airbnb.cn/pg_pixel?r=&diff=16115071061939667863691016617",rootCookies)
    # print(pgPixelCookies)
    # pgPixelCookies = "ssxmod_itna=GqAODK4mx+rxXYj5q7qwxfgQjGknYAzRDBwreiNDnD8x7YDvz8=tzDR2L3qLCq0QWDFOioCttrnAPPp8ggEvrDU4i8DCqYerD43KGwD0eG+DD4DWDmeFDnxAQDjhKGWDb2QDmDimO0DmqG0DDUaj4G2D7tuRihqQkNL/M6qkqAZ00QDjdrD/3wtsCiNxZDM3xQDzdaDtdUyQw6qx0p5WGGbUZhL04DRbPGMFQKDARQKt79qD75uB6448KDlG/hktAmkQAAeGzDkr45mYYqCKgIotiD==; ssxmod_itna2=YqfOYKDKGK+GkDuDl81I5G=vqox0hwAw8xA=u4GCtWxBT1Ox7ppYcgcFyjmOGFteOFL541Zq42eNIPghoDwp0PGcDYF4xD==; bev=1611508165_Nzg3NzIxNTAxMzc5; cdn_exp_bf5e1358597703c51=treatment; cdn_exp_3580f76173e828eaa=treatment; acw_tc=7c8487db16115081673098969e3c07e7c22a2be8a2b1493b75092acdc2; _csrf_token=V4%24.airbnb.cn%240X3DthdMriM%24xRMIhHuXGfgPZnD1CnDlEcI2HTkVfhQ1_NS_1bLacmM%3D; jitney_client_session_id=b5145c08-1717-45c8-9731-ee5966870b5a; jitney_client_session_created_at=1611508167; jitney_client_session_updated_at=1611508167; _user_attributes=%7B%22curr%22%3A%22CNY%22%2C%22guest_exchange%22%3A6.4818999999999996%2C%22device_profiling_session_id%22%3A%221611508167--61e6224792a9d065b4dd6a7f%22%2C%22giftcard_profiling_session_id%22%3A%221611508167--7e9b1d403cf792969d433909%22%2C%22reservation_profiling_session_id%22%3A%221611508167--d01129a7ba80a873ecba2a55%22%7D; flags=0"
    getJson("https://www.airbnb.cn/api/v3/PdpAvailabilityCalendar?operationName=PdpAvailabilityCalendar&locale=zh&currency=CNY&_cb=dilsbk1ai0kf6&variables=%7B%22request%22%3A%7B%22count%22%3A12%2C%22listingId%22%3A%2238253408%22%2C%22month%22%3A1%2C%22year%22%3A2021%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22b94ab2c7e743e30b3d0bc92981a55fff22a05b20bcc9bcc25ca075cc95b42aac%22%7D%7D",pgPixelCookies)




