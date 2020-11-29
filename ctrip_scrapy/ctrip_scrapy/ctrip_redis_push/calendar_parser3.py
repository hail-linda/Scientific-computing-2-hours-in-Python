from parser import Parser
from pymysql.err import InterfaceError
import json
from datetime import datetime
import time


class CalendarParser(Parser):
    def run(self):
        t1 = time.time()
        sql = "SELECT id, house_id, create_time, response FROM house_calendar_response WHERE status=0 " \
              "ORDER BY id ASC LIMIT 1000"

        while True:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()

            t2 = time.time()

            print("query batch response %s" % str(t2-t1))

            if len(rows) < 1:
                break

            t3 = time.time()
            t56 = 0
            t78 = 0

            sql_i = "INSERT IGNORE INTO house_cals (house_date_key, house_id, cal_date, price, " \
                    "booked, price_update_time, booked_update_time) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s) " \
                    "ON DUPLICATE KEY UPDATE price=VALUES(price), booked=VALUES(booked)"

            data_insert = []
            t9 = time.time()
            for r in rows:
                try:
                    t5 = time.time()
                    house_id = r['house_id']
                    ts = r['create_time']
                    response = json.loads(r['response'])
                    _result = json.loads(response['result'])
                    house_cals = _result['data']['houseCalendars']
                    t6 = time.time()
                    t56 += t6-t5
                    t7 = time.time()





                    for hc in house_cals:
                        house_date_key = house_id + "_" + hc['date']
                        booked = 0 if hc['canBooking'] == 1 else 1
                        price = hc['price']

                        data_for_placehold = (house_date_key, house_id, hc['date'], price, booked, ts, ts)
                        data_insert.append(data_for_placehold)
                    t8 = time.time()

                    t78 += t8 - t7


                except Exception as e:
                    self.logger.exception(e)
                    # self.db.rollback()
                    # update_calendar_response_sql = "UPDATE house_calendar_response SET parse_status=2 WHERE id=%s"
                    # self.cursor.execute(update_calendar_response_sql, (r['id'],))
                    # self.db.commit()
                else:
                    pass
                    #TEST
                    # delete_sql = "UPDATE house_calendar_response SET parse_status=1 WHERE id=%s"
                    # # delete_sql = "DELETE house_calendar_response WHERE id=%s"
                    # self.cursor.execute(delete_sql, (r['id'],))
                    # self.db.commit()
            self.cursor.executemany(sql_i, data_insert)
            self.db.commit()
            t10 = time.time()
            print("parse 3 %s" % str(t10-t9))
            print("parse 1 %s" % str(t56))
            print("parse 2 %s" % str(t78))

            t4 = time.time()
            print("parse batch response %s" % str(t4 - t3))


if __name__ == "__main__":
    parser = CalendarParser()
    parser.run()