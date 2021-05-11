import redis
from dbSettings import REDIS_URL
import pymysql
import dbSettings

class detailTask():
    def __init__(self):
        self.db = dbSettings.db_connect()
        self.cursor = self.db.cursor()
        self.listTable = "`houselist_us`"
        self.redis = redis.Redis.from_url(REDIS_URL)
        print(REDIS_URL)


    def insertTask(self):
        # sql = "SELECT `house_id`  FROM `detailresponse_us` WHERE length( `state`)  < 1024"
        sql = "SELECT house_id FROM " + self.listTable 
        self.cursor.execute(sql)
        self.db.commit()

        results = self.cursor.fetchall()

        print(len(results))
        count = 0
        for row in results:
            count += 1
            # self.redis.lpush("detail_us:start_urls", row["house_id"])
            self.redis.lpush("detail_us:start_urls", row["house_id"])
            if count % 10000 == 0:
                print(count)



if __name__ == "__main__":
    task = detailTask()
    task.insertTask()


















































