import redis
from settings import REDIS_URL
from log import get_logger

def redis_conn():
    logger = get_logger()
    try:
        r = redis.Redis.from_url(REDIS_URL)
    except Exception as e:
        logger.exception(e)
    else:
        return r