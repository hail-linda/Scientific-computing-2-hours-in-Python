# -*- coding: UTF-8 -*-

'''
数据需求来源：
    - 上海、张老师
数据导出需求描述：
    - 上海市徐汇区2021-04-30至2021-05-06房源信息及房源
    - 出租情况 listingid 日期 是否出租 价格
    - 房源信息  包括  listingid 经纬度 以及其他的名称所属区域等字段能导出尽量导出
    - listing对方仅仅强调经纬度，我们附加一些title、所属区域等信息即可
    - 价格及订购数据按日区分
数据结构设计：
    1. 房源数据：
        listingid / lat / lng / title / formatted_address / url
        listingDetail.csv
    2. 订房数据：
        listingid / fetch_date / order_date / price / rented
        {
        order_20210430.csv
        ...
        order_20210506.csv
        }

'''

import os
import time
from datetime import date
import pymysql
import dbSettings
import codecs

def dbUtils(sql):
    db = dbSettings.db_connect()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    return cursor.fetchall()

def getOrderPrice(listingId,date):
    sql = '''
    SELECT `order`.`house_id` AS `listingid`,
        `order`.`fetch_date`,
        `order`.`order_date`,
        `price`.`price`,
        'True' AS `rented`
    FROM(
    SELECT `order`.*
    FROM `order`
    LEFT JOIN `cancel` on `order`.`house_id`= `cancel`.`house_id`
    AND `order`.`order_date`= `cancel`.`order_date`
    WHERE `cancel`.`id` IS NULL)  AS `order`
    LEFT JOIN `price` ON `order`.`house_id`= `price` .`house_id`
    AND `order`.`order_date`= `price` .`order_date`
    WHERE `order`.`order_date`= '{}'
    and `order`.`house_id`= '{}'
    ORDER BY `price`.`fetch_date` DESC
    LIMIT 1
    '''.format(date,listingId)
    return dbUtils(sql)

def getPrice(listingId,date):
    sql = '''
    SELECT `house_id` AS `listingid`,
        `fetch_date`AS `fetch`,
        '' AS `fetch_date`,
        `order_date`,
        `price`,
        'False' AS `rented`
    FROM `price`
    WHERE `order_date`= '{}'
    and `house_id`= '{}'
    ORDER BY `fetch` DESC
    limit 1
    '''.format(date,listingId)
    return dbUtils(sql)

def getDetail(listingId):
    sql = '''
    SELECT `detail`.`listingid`,
    `detail`.`Lat` ,
    `detail`.`Lng` ,
    `detail`.`title` ,
    `listing_location`.`formatted_address`  ,
    CONCAT('https://www.airbnb.cn/rooms/',`detail`.`listingid`) AS `url`
    FROM `detail`
    LEFT JOIN `listing_location` ON `detail`.`listingId`= `listing_location`.`listingid`
    WHERE `detail`.`listingId`= '{}'
    '''.format(listingId)
    return dbUtils(sql)

def getListingId():
    sql = "SELECT `listingid`  FROM `listing_location` WHERE `district` ='徐汇区'"
    return dbUtils(sql)

def exportOrder():
    listingIdList = [row['listingid'] for row in getListingId()]
    for date in ['2021-04-30','2021-05-01','2021-05-02','2021-05-03','2021-05-04','2021-05-05','2021-05-06']:
        with open('data/order_{}.csv'.format(date[2:].replace("-","")), 'w',encoding = 'utf-8' ) as f:
            f.write("listingid,fetch_date,order_date,price,rented\n")
            for listingId in listingIdList:
                results = getOrderPrice(listingId,date)
                if len(results) == 0:
                    # print(listingId,date)
                    results = getPrice(listingId,date)
                    # print(results)
                print(results[0])
                row = results[0]
                f.write("{},{},{},{},{}\n".format(row['listingid'],row['fetch_date'],row['order_date'],row['price'],row['rented']))

def convertUTF8ToANSI(oldfile,newfile):
    #打开UTF8文本文件
    f = codecs.open(oldfile,'r','utf8')
    utfstr = f.read()
    f.close()
    
    #把UTF8字符串转码成ANSI字符串
    outansestr = utfstr

    #使用二进制格式保存转码后的文本
    f = open(newfile,'wb','GBK')
    f.write(outansestr)
    f.close()

def exportDetail():
    listingIdList = [row['listingid'] for row in getListingId()]
    with open('data/detailUTF8.csv', 'w',encoding = 'utf-8' ) as f:
        f.write("listingid,Lat,Lng,title,formatted_address,url\n")
        for listingId in listingIdList:
            # print(listingId)
            results = getDetail(listingId)
            if len(results) > 0:
                row = results[0]
                print(row['listingid'],row['title'])
                if not row['title'] == None:
                    row['title'] = row['title'].replace("\n","").replace(",",'，')
                f.write("{},{},{},{},{},{}\n".format(row['listingid'],row['Lat'],row['Lng'],row['title'],row['formatted_address'],row['url']))
            else:
                print(listingId)
    # convertUTF8ToANSI("data/detailUTF8.csv","data/detailANSI.csv")


if __name__ == "__main__":
    # exportOrder()
    exportDetail()
   