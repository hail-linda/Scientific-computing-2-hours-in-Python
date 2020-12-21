import redis
from dbSettings import REDIS_URL
import pymysql

class calendarTask():
    def __init__(self):
        self.db = pymysql.connect(
            "localhost", "root", "delta=b2-4ac", "spideairbnb")
        self.cursor = self.db.cursor()
        self.listTable = "`airbnbspider`.`houselist`"
        self.redis = redis.Redis.from_url(REDIS_URL)
        print(REDIS_URL)


    def insertTask(self):
        sql = "SELECT house_id FROM " + self.listTable 
        self.cursor.execute(sql)
        self.db.commit()

        results = self.cursor.fetchall()

        print(len(results))
        for row in results:
            # house_id = row[0]
            self.redis.lpush("calendar:start_urls", row[0])
            # print(house_id)


if __name__ == "__main__":
    task = calendarTask()
    task.insertTask()


















































