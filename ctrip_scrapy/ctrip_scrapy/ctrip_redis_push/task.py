from redis_db import redis_conn
from db import db_connect
from log import get_logger


class Task(object):
    db, cursor = db_connect()
    redis = redis_conn()
    logger = get_logger()

    def run(self):
        pass



    