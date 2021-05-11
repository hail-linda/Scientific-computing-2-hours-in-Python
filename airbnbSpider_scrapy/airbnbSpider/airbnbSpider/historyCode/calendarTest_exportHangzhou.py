# -*- coding: UTF-8 -*-

import os
import time
from datetime import date
import pymysql
import dbSettings

def dbUtils(sql):
    db = dbSettings.db_connect()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    return cursor.fetchall()

def getOrder(listingId):
    sql = "SELECT * FROM `order` WHERE `house_id` = '{}' and `fetch_date` > '2021-2-20'".format(listingId)
    # print(sql)
    return dbUtils(sql)

def getPrice(listingId,date):
    sql = "SELECT price,fetch_date FROM `price` WHERE house_id = '{}' and order_date ='{}'".format(listingId,date)
    # print(sql)
    try:
        row = dbUtils(sql)[-1]
    except:
        return None
    # print(str(row['fetch_date'])[6])
    if str(row['fetch_date'])[6] == '1':
        return None
    else:
        return row['price']

def getHangZhou():
    sql = "SELECT `listingId` FROM `detail` WHERE lat BETWEEN 30.14987 and 30.4380 and lng BETWEEN 119.95697 and 120.33599"
    return dbUtils(sql)

if __name__ == "__main__":
    with open( '/opt/hangzhou_order_price.csv', 'w',encoding = 'utf-8' ) as f:
        listingIds = [item['listingId'] for item in getHangZhou()]
        count = 0
        for id in listingIds:
            count += 1
            print(count)
            results = getOrder(id)
            for row in results:
                price = getPrice(row['house_id'],row['order_date'])
                if price == None:
                    continue
                f.write("{},{},{},{}\n".format(row['house_id'],row['fetch_date'],row['order_date'],price))
                # print(row['house_id'],row['fetch_date'],row['order_date'],price)
