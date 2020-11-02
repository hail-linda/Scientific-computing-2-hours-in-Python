# -*- coding: UTF-8 -*-

import json
import re
import sqlite3
import threading
import time
from threading import Semaphore, Thread

import chardet
import lxml
import numpy as np
import requests
import scrapy
from lxml import etree
from requests.adapters import HTTPAdapter


def gethtml(url):

    proxies = {
        "http": " http://58.220.95.42:10174",
        "https": "https://58.220.95.42:10174",
    }
    i = 0
    while i < 7:
        try:
            #html = requests.get(url, timeout=5, proxies=proxies)
            html = requests.get(url, timeout=5)
            #print(html.text)
            if("429 Too Many Requests" in html.text):
                print("429 error")
                logFile = open('logFile.html', 'w', encoding='utf-8')
                logFile.write(html.text)
                logFile.close()
            res = json.loads(html.content)
            return html
        except requests.exceptions.RequestException:
            i += 1
        except Exception:
            i += 1
            print(str(Exception))


def getAirbnb(locate, offset=0,price_max=-1,price_min=-1):
    url = "https://www.airbnb.cn/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=true&client_session_id=8865391a-6117-4615-a0d3-b0cc83adc28a&currency=CNY&current_tab_id=home_tab&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=20&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=zh&map_toggle=true&metadata_only=false&place_id=ChIJMzz1sUBwsjURoWTDI5QSlQI&query_understanding_enabled=true&refinement_paths[]=%2Fhomes&satori_config_token=EhIiQhIiIjISEjISIiIiUgA&satori_version=1.1.13&screen_height=425&screen_size=large&screen_width=1472&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=480&version=1.7.9&query=" + str(locate)
    
    url = url.strip()
    time.sleep(0.5)
    if not offset == 0:
        url += "&items_offset="+str(offset)

    if not price_max == -1 and not price_min == -1 :
        url += "&price_max="+str(price_max) 
        url += "&price_min="+str(price_min) 
        print("价格区间："+str(price_min)+" -- "+str(price_max))

    #print(url)
    r = gethtml(url)

    logFile = open('logFile.html', 'w', encoding='utf-8')
    while(r == None):
        print("None")
        r = gethtml(url)
    logFile.write(r.text)
    logFile.close()
    count = 1000
    try:
        res = json.loads(r.content)
    except Exception:
        print(Exception, "getHTML", time.asctime(time.localtime(time.time())))
        print(count, offset)
        getAirbnb(locate, offset)
        if(count-offset > 50):
            # ime.sleep(1)
            getAirbnb(locate, offset+50)
        return

    if 'home_tab_metadata' in res['explore_tabs'][0]:
        count = res['explore_tabs'][0]['home_tab_metadata']['listings_count']
        if(count > 300):
            if(price_max == -1 or price_min == -1):
                print("房源数："+str(count)+"  min:0  max:5000")
                getAirbnb(locate,price_max=5000,price_min=0)
            else :
                print("房源数："+str(count)+"  min:"+str(price_min)+"  max:"+str(price_max))
                midd = int(0.5*(price_max+price_min))
                getAirbnb(locate,price_max=midd,price_min=price_min)
                getAirbnb(locate,price_max=price_max,price_min=midd)
                
            return
    else:
        print("房源总数未知")


    sections = res['explore_tabs'][0]['sections']
    conn_temp = sqlite3.connect("./airbnbSpider.db")
    cur_temp = conn_temp.cursor()
    for section in sections:
        exist = 0
        insert = 0
        if 'listings' in section:
            listings = section['listings']

            inDB = ""
            for listing in listings:
                try:
                    price = listing['pricing_quote']['price_string']
                    description = listing['listing']['name']
                    house_id = listing['listing']['id']
                    # print(house_id)
                    description = description.replace("'", "''")
                    description = description.replace('"', '""')
                    # print(price,description)
                    sql = 'SELECT * FROM housing WHERE house_id = ' + \
                        str(house_id)
                    # print(sql)
                    cur_temp.execute(sql)
                    conn_temp.commit()
                    if not cur_temp.fetchone():
                        sql = ("INSERT INTO housing VALUES (NULL ,'%s','%s','%s','%s')") % (
                            locate, price, description, house_id)
                        cur_temp.execute(sql)
                        conn_temp.commit()
                        #print("     -------INSERT-------")
                        insert += 1
                        inDB += "-"
                    else:
                        exist += 1
                        inDB += "$"
                except Exception as e:
                    print(str(e), "for listing", time.asctime(
                        time.localtime(time.time())))
                    getAirbnb(locate, offset)
                    pass
            print("数量："+str(len(listings)),
                  time.asctime(time.localtime(time.time())))
            print("共{}个，其中重复{}，新增{},{}".format(
                str(len(listings)), exist, insert, inDB))
    conn_temp.close()

    print(count, offset, locate)
    if(count-offset > 50):
        # time.sleep(1)
        getAirbnb(locate, offset+50)


def main():
    sem = threading.Semaphore(3)
    conn = sqlite3.connect("./airbnbSpider.db")
    cur = conn.cursor()
    flag = 1
    sql = 'SELECT * FROM administrativeDivision WHERE level = 3'
    cur_locate_3 = conn.cursor()
    cur_locate_3.execute(sql)
    conn.commit()
    locates = []
    for row3 in cur_locate_3:
        name = row3[2]
        code = row3[3]
        sql = 'SELECT * FROM administrativeDivision WHERE code = ' + \
            str(code)[:4]+"00000000"
        cur_locate_2 = conn.cursor()
        cur_locate_2.execute(sql)
        conn.commit()
        for row2 in cur_locate_2:
            name = "上海市"+row2[2]+name
            name = name.replace("市辖区", "")
            # print(name)
            if(flag == 1):
                locates.append(name)

    conn.close()

    locates.append("上海市")

    for locate in locates:

        getAirbnb(locate)


'''
    print(locate)
    sem.acquire()
    thread_run = threading.Thread(target=getAirbnb , args=(name,))
    thread_run.start()
    print("锁数量："+str(sem._value))
    sem.release()
'''


if __name__ == "__main__":
    main()
