from parser import Parser
from pymysql.err import InterfaceError
import json
from datetime import datetime
import time
from qqmail import QQMail
from settings import EMAIL_NAME, EMAIL_PWD, EMAIL_SENDER, EMAIL_RECIPIENTS
from redis_db import redis_conn


class CalendarParser(Parser):
    table_response = "jdtest_house_calendar_response"
    table_calendar = "jdtest_house_cals"
    # table_response = "house_calendar_response"
    # table_calendar = "house_cals"
    limit = "10000"
    error_threshold = 1000
    error_count = 0
    error_sent = False
    def run(self):
        sql = "SELECT id, house_id, create_time, response FROM " + self.table_response + " WHERE status=0 " \
              "ORDER BY id ASC LIMIT " + self.limit
        sql_delete = "DELETE FROM " + self.table_response + " ORDER BY id ASC LIMIT " + self.limit

        rnd = 0

        while True:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()

            if len(rows) < 1:
                break

            rnd += 1
            print(rnd * int(self.limit))

            sql_i = "INSERT IGNORE INTO " + self.table_calendar + " (house_date_key, house_id, cal_date, price, " \
                    "booked, booked_update_time) " \
                    "VALUES (%s, %s, %s, %s, %s, %s)"

            data_insert = []
            for r in rows:
                try:
                    house_id = r['house_id']
                    ts = r['create_time']
                    response = json.loads(r['response'])
                    _result = json.loads(response['result'])
                    house_cals = _result['data']['houseCalendars']

                    for hc in house_cals:
                        booked = 0 if hc['canBooking'] == 1 else 1
                        house_date_key = house_id + "_" + hc['date'] + "_" + str(booked)
                        price = int(hc['price'] * 100)

                        data_for_placehold = (house_date_key, house_id, hc['date'], price, booked, ts)
                        data_insert.append(data_for_placehold)


                except Exception as e:
                    self.logger.exception(e)
                    self.error_count += 1
                    # @TODO: if too many exceptions are caught, can we delete the original responses?
                    if self.error_count > self.error_threshold and not self.error_sent:
                        qqm = QQMail(EMAIL_SENDER, EMAIL_PWD, EMAIL_NAME)
                        qqm.send(EMAIL_RECIPIENTS, "Error occurs while parsing calendar", str(e))
                        self.error_sent = True

            """ Stop parsing while too many errors
            """
            if self.error_count > self.error_threshold:
                self.logger.error("Stop parsing while too many errors")
                break

            try:
                self.cursor.executemany(sql_i, data_insert)
            except Exception as e:
                self.logger.exception(e)
            else:
                """Be careful!!! Responses will be deleted.
                """
                self.cursor.execute(sql_delete)
                self.db.commit()

    @staticmethod
    def is_listing_spider_working():
        rds = redis_conn()
        n = rds.lrange('listing', start=0, end=1)
        if len(n) > 0:
            return True
        else:
            return False




if __name__ == "__main__":
    # parser = CalendarParser()
    # parser.run()
    print(CalendarParser.is_listing_spider_working())