import redis , time
from dbSettings import REDIS_URL
import pymysql
import dbSettings

class Monitor():
    def __init__(self):
        self.db = dbSettings.db_connect()
        self.cursor = self.db.cursor()
        self.listTable = "`houselist`"
        self.redis = redis.Redis.from_url(REDIS_URL)
        print(time.asctime( time.localtime(time.time()) ))

    def checkRedis(self):
        return self.redis.llen("calendar:start_urls")
    
    def checkMYSQLcalendarResponse(self):
        sql = "SELECT MAX(id) FROM calendarresponse"
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        len = results[0]["MAX(id)"] 
        if len == None :
            len = 0
        return len


    def innerTask(self):
        redisLen1 = self.checkRedis()
        responseLen1 = self.checkMYSQLcalendarResponse()
        print(redisLen1,responseLen1)
        time.sleep(120)
        redisLen2 = self.checkRedis()
        responseLen2 = self.checkMYSQLcalendarResponse()
        print(redisLen2,responseLen2)

        isRedisworking      = False if (redisLen1 - redisLen2 == 0) else True
        isResponseworking   = False if (responseLen1 - responseLen2 == 0) else True

        isRedisRunOut       = True if redisLen2 == 0 else False
        isResponseRunOut    = True if responseLen2 == 0 else False


        state = []

        if isRedisRunOut and isRedisRunOut :
            state.append("sleeping")
        if isRedisworking and isResponseworking:
            state.append("crawling")
        if (not isRedisRunOut) and (not isRedisworking):
            state.append("err:notCrawling")
        if
        





if __name__ == "__main__":
    task = Monitor()
    task.innerTask()


















































