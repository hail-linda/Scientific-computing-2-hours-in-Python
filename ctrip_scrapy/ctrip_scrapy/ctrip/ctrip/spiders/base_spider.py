from ctrip import db
from scrapy_redis.spiders import RedisSpider
import logging
from ctrip.settings import LOG_LEVEL

class BaseSpider(RedisSpider):

    logging.getLogger().addHandler(logging.StreamHandler())
    db, cursor = db.db_connect()

    # def __init__(self):
    #     """Adds db connection object into spider instance, so that we can retrieve db connection
    #     from spider object
    #     """
    #
    #     self.db, self.cursor = db.db_connect()
    #     self.logger.debug("Db connection established.")

    def __del__(self):
        self.db.close()
        self.logger.debug("Db connection closed.")