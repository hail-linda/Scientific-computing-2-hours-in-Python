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
from dbSettings import REDIS_URL



class calendarParse():
    def __init__(self):
        self.table = "`proxypool`"
        self.db = dbSettings.db_connect()
        self.cursor = self.db.cursor()
        self.redis = redis.Redis.from_url(REDIS_URL)
        self.mapTable = "`map`"
        self.listTable = "`houselist`"
        self.mapresponseTable = "`mapresponse`"
        self.calendarresponseTable = "`calendarresponse`"

        localtime = time.localtime(time.time())
        self.mouth = localtime[1]
        self.year = localtime[0]
        self.day = localtime[2]-1
        self.dtToday = "{}-{}-{}".format(self.year, self.mouth, self.day)

        self.orderList = []
        self.priceList = []
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
                res = row["response"].replace("''", "'")
                res = res.replace('""', '"')
            except:
                print("replace err in ", row["id"])
                errIdList.append(row["id"])
                continue

            if "429 Too Many" in res:
                self.redis.lpush("calendar:start_urls", row["house_id"])
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
            if 'calendar_months' in res:
                for month in res['calendar_months']:
                    for day in month['days']:
                        if self.dateCompare(self.dtToday, day['date']) < 0:
                            try:
                                self.priceList.append(
                                    [day['date'], day['price']['local_price_formatted']])
                                if day['available'] == False:
                                    self.orderList.append(day['date'])
                            except:
                                
                                continue

        self.dbInsert()
        self.priceList = []
        self.orderList = []
        return errIdList

    def dbInsert(self):
        self.vals = []
        self.sql = "INSERT IGNORE INTO `order` (`house_id`, `fetch_date`, `order_date`, repeat_flag)\
                    VALUES (%s,%s,%s,%s);"
        for order in self.orderList:
            repeat_flag = "{}:{}".format(self.house_id, order)
            # print(self.house_id,self.dtToday,order,hash)
            self.vals.append((self.house_id, self.dtToday, order, repeat_flag))

        self.cursor.executemany(self.sql, self.vals)
        self.db.commit()
        self.orderAffected = self.cursor.rowcount

        self.vals = []
        self.sql = "INSERT IGNORE INTO `price` (`house_id`, `fetch_date`, `order_date`,`price`, repeat_flag)\
        VALUES (%s,%s,%s,%s,%s);"

        for price in self.priceList:
            orderDate = price[0]
            price = price[1]
            repeat_flag = "{}:{}:{}".format(self.house_id, order, price)
            self.vals.append(
                (self.house_id, self.dtToday, orderDate, price, repeat_flag))

        self.cursor.executemany(self.sql, self.vals)
        self.db.commit()
        self.priceAffected = self.cursor.rowcount

        # print("sqlId:{}\thouse_id: {}\t order insert {} in {} \tprice insert {} in {} \
        #     ".format(self.sqlId,self.house_id,self.orderAffected,len(self.orderList),self.priceAffected,len(self.priceList)))


def parseStart(bias):
    try:
        parse = calendarParse()
        return parse.getItem(bias)
    except Exception as e:
        print(e)

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



if __name__ == "__main__":
    # 数据库链接
    db = dbSettings.db_connect()
    cursor = db.cursor()

    # # 起始responseId
    # startResponseId = 0
    # sql = "SELECT * FROM `calendarparselog` where type = 'end parse' order by id desc limit 1"
    # cursor.execute(sql)
    # db.commit()
    # # print(int(cursor.fetchall()[0]["response_id"]))
    # try:
    #     startResponseId = cursor.fetchall()[0]["response_id"]
    # except:
    #     pass
    startResponseId = 0
        

    # 结束responseId
    endResponseId = getMaxNumOfCalendarResponse(db,cursor)

    print("start parse at {}".format(startResponseId))

    errResponseIdList = []

    # start parse
    dbInsertparselog("start parse",startResponseId,"None")

    for responseId in range(startResponseId, endResponseId,1000):
        errResponseIdList += parseStart(responseId)
        print(len(errResponseIdList))
        if(len(errResponseIdList)>30000):
            break
    # end parse
    dbInsertparselog("end parse",responseId,"None")

    # err report
    if len(errResponseIdList) > 30000:
        dbInsertparselog("too much error,break",responseId,json.dumps(errResponseIdList))
    elif len(errResponseIdList) > 1:
        dbInsertparselog("err log",responseId,json.dumps(errResponseIdList))

    if len(errResponseIdList) < 30000:
        sql = "TRUNCATE TABLE `calendarresponse`;"
        cursor.execute(sql)
        db.commit()
        dbInsertparselog("truncate",0,"truncate calendarResponse")



    

        
    

