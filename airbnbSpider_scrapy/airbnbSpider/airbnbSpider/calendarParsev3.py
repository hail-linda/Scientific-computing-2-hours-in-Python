# -*- coding: UTF-8 -*-

import os
import time
import random
import json
import re
import time
import pymysql
import dbSettings
import scrapy
import redis
import psutil
from dbSettings import REDIS_URL
from monitor import Monitor



class calendarParse():
    def __init__(self,cancelList,localtime):
        self.table = "`proxypool`"
        self.db = dbSettings.db_connect()
        self.cursor = self.db.cursor()
        self.mapTable = "`map`"
        self.listTable = "`houselist`"
        self.mapresponseTable = "`mapresponse`"
        self.calendarresponseTable = "`calendarresponse`"
        self.cancelList = cancelList


        self.mouth = localtime[1]
        self.year = localtime[0]
        self.day = localtime[2]
        self.dtToday = "{}-{}-{}".format(self.year, self.mouth, self.day)

        self.orderList = []
        self.priceList = []
        self.todayCancelList = []
        self.canceledList = []
        self.house_id = 0


    def __del__(self):
        self.db.close()

    def dateCompare(self, dt1, dt2):
        dt1 = time.mktime(time.strptime(dt1, '%Y-%m-%d'))
        dt2 = time.mktime(time.strptime(dt2, '%Y-%m-%d'))
        return dt1-dt2

    def getItem(self, bias):
        self.priceList = []
        self.orderList = []
        self.todayCancelList = []
        errIdList = []


        sql = "SELECT * FROM " + self.calendarresponseTable + \
            "WHERE id between {} and {}".format(bias, bias+1000)
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        for row in results:
            try:
                self.sqlId = row["id"]
                self.house_id = row["house_id"]
                res = row["response"]
            except:
                print("replace err in ", row["id"])
                errIdList.append(row["id"])
                continue

            if "429 Too Many" in res:
                # self.redis.lpush("calendar:start_urls", row["house_id"])
                print("429 err in ", row["id"])
                errIdList.append(row["id"])
                continue

            try:
                res = json.loads(res, strict=False)
            except Exception as e:
                print(e)
                print("json.loads err in {}".format(row["id"]))
                errIdList.append(row["id"])
                continue

            # if 'metadata' in res:
            #     if not 'first_bookable_day' in res['metadata']:
            #         return
            num = 0
            if "errors" in res:
                errIdList.append(row["id"])
                continue
            if 'data' not in res:
                print(self.sqlId,"have no data")
                continue

            pdpAvailabilityCalendar = res['data']['merlin']['pdpAvailabilityCalendar']
            for month in pdpAvailabilityCalendar["calendarMonths"]:
                for day in month["days"]:
                    available = day["available"]
                    date = day["calendarDate"]
                    price = day["price"]["localPriceFormatted"]

                    if self.dateCompare(self.dtToday, date) <= 0:
                        try:
                            self.priceList.append([date, price.replace(",","").replace("￥","")])
                            if available == False:
                                self.orderList.append(date)
                            if self.dateCompare(self.dtToday, date) == 0 and available == True :
                                self.todayCancelList.append(date)
                        except:
                            # print("price append err")
                            continue

            self.dbInsert()
            self.priceList = []
            self.orderList = []
            self.todayCancelList = []
        
        print("len of canceledList:\t",len(self.canceledList))
        return errIdList

    def dbInsert(self):

        # print(self.house_id,self.orderList)
        # print(self.house_id,self.priceList)
        # print('\n')
        self.vals = []
        self.sql = "INSERT IGNORE INTO `order` (`house_id`, `fetch_date`, `order_date`, repeat_flag)\
                    VALUES (%s,%s,%s,%s);"
        for order in self.orderList:
            # self.dtToday = "{}-{}-{}".format(self.year, self.mouth, self.day-random.randint(0,1))###################################
            repeat_flag = "{}:{}".format(self.house_id, order)
            # print(self.house_id,self.dtToday,order,hash)
            self.vals.append((self.house_id, self.dtToday, order, repeat_flag))
        self.cursor.executemany(self.sql, self.vals)
        self.db.commit()
        self.orderAffected = self.cursor.rowcount

        self.vals = []
        self.sql = "INSERT IGNORE INTO `cancel` (`house_id`, `fetch_date`, `order_date`, repeat_flag)\
                    VALUES (%s,%s,%s,%s);"
        for order in self.todayCancelList :
            # self.dtToday = "{}-{}-{}".format(self.year, self.mouth, self.day-random.randint(0,1))###################################
            repeat_flag = "{}:{}".format(self.house_id, order)
            # print(self.house_id,self.dtToday,order,hash)
            # print(repeat_flag,self.cancelList[1])
            if repeat_flag in self.cancelList:
                self.canceledList.append(self.house_id)
                self.vals.append((self.house_id, self.dtToday, order, repeat_flag))
        self.cursor.executemany(self.sql, self.vals)
        self.db.commit()
        self.orderAffected = self.cursor.rowcount

        self.vals = []
        self.sql = "INSERT IGNORE INTO `price` (`house_id`, `fetch_date`, `order_date`,`price`, repeat_flag)\
        VALUES (%s,%s,%s,%s,%s);"

        for price in self.priceList:
            # self.dtToday = "{}-{}-{}".format(self.year, self.mouth, self.day-random.randint(0,1))###############################
            orderDate = price[0]
            price = price[1]
            repeat_flag = "{}:{}:{}".format(self.house_id, orderDate, price)
            self.vals.append(
                (self.house_id, self.dtToday, orderDate, price, repeat_flag))

        self.cursor.executemany(self.sql, self.vals)
        self.db.commit()
        self.priceAffected = self.cursor.rowcount

        # print("sqlId:{}\thouse_id: {}\t order insert {} in {} \tprice insert {} in {} \
        #     ".format(self.sqlId,self.house_id,self.orderAffected,len(self.orderList),self.priceAffected,len(self.priceList)))

def dbInsertparselog(type,responseId,infor):
    # 数据库链接
    db = dbSettings.db_connect()
    cursor = db.cursor()

    sql = "INSERT IGNORE INTO `calendarparselog` (`type`, `response_id`, `infor`)\
           VALUES ('{}',{},'{}');".format(type,responseId,infor)
    print(sql)
    cursor.execute(sql)
    db.commit()



def getMaxNumOfCalendarResponse(db,cursor):
    sql = "SELECT MAX(id) FROM `calendarresponse` order by id desc limit 1"
    cursor.execute(sql)
    db.commit()
    num = cursor.fetchall()[0]["MAX(id)"]
    return num


MODE = 'DEBUG'
MODE = 'PRODUCT'

if __name__ == "__main__":
    if MODE == 'PRODUCT':
        monitor = Monitor()
        if not monitor.innerTask() :
            print("calendarParsev3:do not start Parse")
            quit()


    # 数据库链接
    db = dbSettings.db_connect()
    cursor = db.cursor()
    print("get cancelList")
    cursor.execute("SELECT `house_id`, `order_date`  FROM `order` WHERE `order_date` = CURRENT_DATE ")
    results = cursor.fetchall()
    cancelList = []

    for row in results:
        cancelList.append("{}:{}".format(row['house_id'],row['order_date']))

    print("len of cancelList:",len(cancelList))
    print(u'当前进程的内存使用：%.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 )) 


    startResponseId = 0

    # 结束responseId
    endResponseId = getMaxNumOfCalendarResponse(db,cursor)

    print("start parse at {}".format(startResponseId))

    errResponseIdList = []

    # start parse
    if MODE == 'PRODUCT':
        dbInsertparselog("start parse",startResponseId,"None")

    parse = calendarParse(cancelList,time.localtime(time.time()))
    for responseId in range(startResponseId, endResponseId+1,1000):
        errResponseIdList += parse.getItem(responseId)
        print("len of errList:\t",len(errResponseIdList))
        if(len(errResponseIdList)>100000):
            break
    # end parse
    dbInsertparselog("end parse",endResponseId,"None")

    # err report
    if len(errResponseIdList) > 100000:
        dbInsertparselog("too much error,break",responseId,json.dumps(errResponseIdList))
    elif len(errResponseIdList) > 1:
        dbInsertparselog("err log",responseId,json.dumps(errResponseIdList))

    if len(errResponseIdList) < 100000:
        sql = "TRUNCATE TABLE `calendarresponse`;"
        cursor.execute(sql)
        db.commit()
        dbInsertparselog("truncate",0,"truncate calendarResponse")



    

        
    

