# -*- coding: UTF-8 -*-
import  json

# import dbSettings
import requests

# def getListingId():
#     db = dbSettings.db_connect()
#     cursor = db.cursor()

#     sql = "SELECT house_id FROM `houselist_us` ORDER BY RAND() LIMIT 30000"
#     cursor.execute(sql)
#     db.commit()
#     result = cursor.fetchall()
#     return [i['house_id'] for i in result]


if __name__ == "__main__":
    # f = open("houseId30K.txt", 'w')
    # li = getListingId()
    # print(len(li))
    # print(json.dumps(li),file=f)

    f = open("houseId30K.txt", 'r')
    houseList = json.loads(f.readline())
    for i in houseList:
        print(i)