# Scrapy settings for ctrip project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from ctrip import const, user_agent
import random

ENV = const.ENV_PRODUCT

if const.ENV_DEVELOP == ENV:
    # local mysql server
    MYSQL_CONFIG = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "123456",
        "port": 3306,
        "db": "ctrip_scrapy",
        "charset": "UTF8MB4",
    }

    # REDIS_URL = 'redis://:password@127.0.0.1:6379/0'
    REDIS_URL = 'redis://:{psw}@{host}:{port}/{db}'.format(
        host='127.0.0.1',
        port='6379',
        psw='',
        db=0
    )

    LOG_LEVEL = 'INFO'
elif const.ENV_PRODUCT == ENV:
    LOG_LEVEL = 'ERROR'
    # mysql server
    MYSQL_CONFIG = {
        "host": "rm-2zesd1dlom704lm0a125010.mysql.rds.aliyuncs.com",
        "user": "daduosu",
        "password": "Daduosu@)@)",
        "port": 3306,
        "db": "ctrip_scrapy",
        "charset": "UTF8MB4",
    }

    # REDIS_URL = 'redis://:password@127.0.0.1:6379/0'
    REDIS_URL = 'redis://:{psw}@{host}:{port}/{db}'.format(
        host='r-2zeryyjl6mne2qqzhd.redis.rds.aliyuncs.com',
        port='6379',
        psw='Daduosu@)@)',
        db=0
    )
else:
    # remote mysql server
    pass

    # MYSQL_CONFIG = {
    #     "host": "127.0.0.1",
    #     "user": "root",
    #     "password": "123456",
    #     "port": 3306,
    #     "db": "ctrip_scrapy",
    #     "charset": "UTF8MB4",
    # }


    # REDIS_URL = 'redis://:{psw}@{host}:{port}/{db}'.format(
    #     host='127.0.0.1',
    #     port='6379',
    #     psw='',
    #     db=0
    # )



LOG_FILE = 'logs/spider.log'
LOG_FORMAT = '%(levelname)s %(asctime)s [%(name)s:%(module)s:%(funcName)s:%(lineno)s] [%(exc_info)s] %(message)s'

BOT_NAME = 'ctrip'

SPIDER_MODULES = ['ctrip.spiders']
NEWSPIDER_MODULE = 'ctrip.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = random.choice(user_agent.agents)

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'ctrip.middlewares.CtripSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'ctrip.middlewares.CtripDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'ctrip.pipelines.CtripPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# Ensure use this Scheduler
SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis
DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"

# Number of Hash Functions to use, defaults to 6
BLOOMFILTER_HASH_NUMBER = 6

# Redis Memory Bit of Bloomfilter Usage, 30 means 2^30 = 128MB, defaults to 30
BLOOMFILTER_BIT = 30

# Persist
SCHEDULER_PERSIST = True