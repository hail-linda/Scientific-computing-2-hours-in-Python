import redis
from dbSettings import REDIS_URL
import pymysql
import dbSettings

class calendarTask():
    def __init__(self):
        self.db = dbSettings.db_connect()
        self.cursor = self.db.cursor()
        self.listTable = "`houselist`"
        self.calendarResponseTable = "`calendarresponse`"
        self.redis = redis.Redis.from_url(REDIS_URL)
        print(REDIS_URL)


    def insertTask(self):
        ENV = "PRODUCT"
        ENV = "APPEND"
        if ENV == "APPEND":
            sql = "SELECT house_id FROM " + self.calendarResponseTable
            self.cursor.execute(sql)
            self.db.commit()
            results = self.cursor.fetchall()
            existResponseList = {row['house_id'] for row in results}
            existRedisList = self.redis.lrange("calendar:start_urls",0,-1)
            existRedisList = {i.decode() for i in existRedisList}
            existResponseList = existResponseList | existRedisList
            print(len(existResponseList))

        sql = "SELECT house_id FROM " + self.listTable 
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        print(len(results))



        count = 0
        appendCount = 0
        for row in results:
            count += 1
            if ENV == "APPEND" and row["house_id"] not in existResponseList:
                self.redis.lpush("calendar:start_urls", row["house_id"])
                appendCount += 1
            elif ENV == "PRODUCT":
                self.redis.lpush("calendar:start_urls", row["house_id"])
            if count % 10000 == 0:
                print(count)
                print(appendCount)



if __name__ == "__main__":
    task = calendarTask()
    task.insertTask()


















































