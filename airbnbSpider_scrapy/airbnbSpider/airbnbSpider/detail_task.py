import redis
from dbSettings import REDIS_URL
import pymysql
import dbSettings

class detailTask():
    def __init__(self):
        self.db = dbSettings.db_connect()
        self.cursor = self.db.cursor()
        self.listTable = "`houselist`"
        self.detailTable = "`detail`"
        self.redis = redis.Redis.from_url(REDIS_URL)
        print(REDIS_URL)


    def insertTask(self):
        sql = "SELECT listingId FROM " + self.detailTable
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        existDetailList = {str(row['listingId']) for row in results}
        print(len(existDetailList))

        sql = "SELECT house_id FROM " + self.listTable 
        self.cursor.execute(sql)
        self.db.commit()

        results = self.cursor.fetchall()

        print(len(results))
        count = 0
        pushCount = 0
        for row in results:
            
            count += 1
            if str(row["house_id"]) not in existDetailList:
                self.redis.lpush("detail:start_urls", row["house_id"])
                pushCount += 1
            if count % 10000 == 0:
                print(count,pushCount)



if __name__ == "__main__":
    task = detailTask()
    task.insertTask()


















































