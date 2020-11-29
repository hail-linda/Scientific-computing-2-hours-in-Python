from settings import MYSQL_CONFIG
import pymysql
from log import get_logger

def db_connect():
    logger = get_logger()
    try:
        connection = pymysql.connect(host=MYSQL_CONFIG['host'], user=MYSQL_CONFIG['user'],
                                     password=MYSQL_CONFIG['password'], db=MYSQL_CONFIG['db'],
                                     port=MYSQL_CONFIG['port'], charset=MYSQL_CONFIG['charset'],
                                     cursorclass=pymysql.cursors.DictCursor)
        # connection.autocommit(True)
    except pymysql.OperationalError as e:
        logger.exception(e)
    else:
        cursor = connection.cursor()
        return connection, cursor