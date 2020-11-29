from ctrip.settings import MYSQL_CONFIG
import pymysql, logging

def db_connect():
    try:
        connection = pymysql.connect(host=MYSQL_CONFIG['host'], user=MYSQL_CONFIG['user'],
                                     password=MYSQL_CONFIG['password'], db=MYSQL_CONFIG['db'],
                                     port=MYSQL_CONFIG['port'], charset=MYSQL_CONFIG['charset'],
                                     cursorclass=pymysql.cursors.DictCursor)
        # connection.autocommit(True)
    except pymysql.OperationalError as e:
        logging.exception(str(e))
        return None, None
    else:
        cursor = connection.cursor()
        return connection, cursor