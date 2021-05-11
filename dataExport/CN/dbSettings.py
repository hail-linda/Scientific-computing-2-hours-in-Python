import pymysql
import logging

ENV_DEVELOP = "DEVELOP"
ENV_PRODUCT = "PRODUCT"


ENV = ENV_DEVELOP
ENV = ENV_PRODUCT

MYSQL_CONFIG_DEVELOP = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "delta=b2-4ac",
    "port": 3306,
    "db": "airbnbspider"
}

REDIS_URL_DEVELOP = 'redis://:{psw}@{host}:{port}/{db}'.format(
    host='r-2zeryyjl6mne2qqzhdpd.redis.rds.aliyuncs.com',
    port='6379',
    psw='Daduosu@)@)',
    db=0
)

MYSQL_CONFIG_PRODUCT = {
    "host": "rm-2zesd1dlom704lm0a125010.mysql.rds.aliyuncs.com",
    "user": "airbnb_spider",
    "password": "09wLjYSgWapXXD1f",
    "port": 3306,
    "db": "airbnb_scrapy"
}

# mysql -hrm-2zesd1dlom704lm0a125010.mysql.rds.aliyuncs.com -uairbnb_spider -p09wLjYSgWapXXD1f

REDIS_URL_PRODUCT = 'redis://:{psw}@{host}:{port}/{db}'.format(
    host='r-2zeryyjl6mne2qqzhd.redis.rds.aliyuncs.com',
    port='6379',
    psw='Daduosu@)@)',
    db=0
)

if ENV == ENV_PRODUCT :
    MYSQL_CONFIG = MYSQL_CONFIG_PRODUCT
    REDIS_URL   = REDIS_URL_PRODUCT
elif ENV == ENV_DEVELOP :
    MYSQL_CONFIG = MYSQL_CONFIG_DEVELOP
    REDIS_URL   = REDIS_URL_DEVELOP

def db_connect():
    try:
        connection = pymysql.connect(host=MYSQL_CONFIG['host'], user=MYSQL_CONFIG['user'],
                                     password=MYSQL_CONFIG['password'], db=MYSQL_CONFIG['db'],
                                     port=MYSQL_CONFIG['port'],
                                     charset="utf8mb4",
                                     cursorclass=pymysql.cursors.DictCursor)
    except pymysql.OperationalError as e:
        logging.exception(str(e))
        return None
    return connection
