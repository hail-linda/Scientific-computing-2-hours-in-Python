from db import db_connect
from log import get_logger


class Parser(object):
    db, cursor = db_connect()
    logger = get_logger()

    def run(self):
        pass


    def handle_db_timeout(self, sql, params, e):    
        """Reconnect db when db connection timeout."""
        self.logger.info("database connection timeout, reconnect")
        self.logger.exception(e)
        self.db.ping(reconnect=True)
        self.cursor.execute(sql, params)
        self.db.commit()