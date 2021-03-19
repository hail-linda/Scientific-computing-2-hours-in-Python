import redis , time, datetime
from dbSettings import REDIS_URL
import pymysql
import dbSettings
from SMTP import SMTP

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
    
    def parseState(self):
        sql = "SELECT * FROM `calendarparselog` WHERE `type` = 'start parse' ORDER BY id desc limit 1 "
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        startParseId = results[0]["id"] 
        diffStartParseTime = (datetime.datetime.now() - results[0]["msg_time"]).seconds

        sql = "SELECT * FROM `calendarparselog` WHERE `type` = 'end parse' ORDER BY id desc limit 1 "
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        endParseId = results[0]["id"] 

        print(diffStartParseTime/3600)   

        if endParseId > startParseId :
            return "waitting"
        elif diffStartParseTime/3600 < 4:
            return "parseing"
        else :
            return "err in  parseing"

    def innerTask(self):
        redisLen1 = self.checkRedis()
        responseLen1 = self.checkMYSQLcalendarResponse()
        print(redisLen1,responseLen1)

        print("time.sleep:",end = '')
        for i in range(60):
            print(i)
            time.sleep(1)
        redisLen2 = self.checkRedis()
        responseLen2 = self.checkMYSQLcalendarResponse()
        print(redisLen2,responseLen2)

        isRedisworking      = False if (redisLen1 - redisLen2 == 0) else True
        isResponseworking   = False if (responseLen1 - responseLen2 == 0) else True

        isRedisRunOut       = True if redisLen2 == 0 else False
        isResponseRunOut    = True if responseLen2 == 0 else False

        isParseing          = self.parseState()
        if isParseing == "err in  parseing":
            SMTP("1282255404@qq.com","发信内容","calendar Parse 时间过长","DaduosuMonitor")
            return

        isParseing          = True if isParseing == "parseing" else False
        state = []

        if isRedisRunOut and isResponseRunOut :
            state.append("sleeping")
        if isRedisworking and isResponseworking:
            state.append("crawling")
        if (not isRedisRunOut) and (not isRedisworking):
            SMTP("1282255404@qq.com","发信内容","未正常爬取","DaduosuMonitor")
            state.append("err:notCrawling")
            return False
        if isRedisRunOut and (not isResponseRunOut) and (not isParseing):
            state.append("need Parse")
            SMTP("1282255404@qq.com","发信内容","开始解析：{}"。format(responseLen2),"DaduosuMonitor")
            return True

        print("Monitor:",state,isParseing)
        return False
        


if __name__ == "__main__":
    task = Monitor()
    task.innerTask()


















































