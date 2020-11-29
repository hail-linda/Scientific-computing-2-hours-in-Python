from parser import Parser
from pymysql.err import InterfaceError
import json
from datetime import datetime


class CalendarParser(Parser):
    def run(self):
        sql = "SELECT id, house_id, create_time, response FROM house_calendar_response WHERE status=0 AND parse_status=0 " \
              "ORDER BY id ASC LIMIT 1000"

        while True:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()

            if len(rows) < 1:
                break

            for r in rows:
                try:
                    house_id = r['house_id']
                    ts = r['create_time']
                    response = json.loads(r['response'])
                    _result = json.loads(response['result'])
                    house_cals = _result['data']['houseCalendars']
                    if isinstance(house_cals, list):
                        for hc in house_cals:
                            house_date_key = house_id + "_" + hc['date']
                            booked = 0 if hc['canBooking'] == 1 else 1
                            price = hc['price']

                            sql_q = "SELECT * FROM house_cals WHERE house_date_key=%s"
                            self.cursor.execute(sql_q, (house_date_key,))
                            rows_q = self.cursor.fetchall()
                            if len(rows_q) > 0:
                                row_o = rows_q[0]
                                price_o = row_o['price']
                                booked_o = row_o['booked']

                                price_updated = 0
                                booked_updated = 0

                                if float(price) != float(price_o):
                                    price_updated = 1

                                if booked != booked_o:
                                    booked_updated = 1

                                if price_updated == 1 and booked_updated == 0:
                                    sql_u = "UPDATE house_cals SET price=%s, price_update_time=%s " \
                                            "WHERE house_date_key=%s"
                                    data_for_placehold = (price, ts, house_date_key)
                                    self.cursor.execute(sql_u, data_for_placehold)
                                if price_updated == 0 and booked_updated == 1:
                                    sql_u = "UPDATE house_cals SET booked=%s, booked_update_time=%s " \
                                            "WHERE house_date_key=%s"
                                    data_for_placehold = (booked, ts, house_date_key)
                                    self.cursor.execute(sql_u, data_for_placehold)
                                if price_updated == 1 and booked_updated == 1:
                                    sql_u = "UPDATE house_cals SET price=%s, booked=%s, price_update_time=%s, " \
                                            "booked_update_time=%s WHERE house_date_key=%s"
                                    data_for_placehold = (price, booked, ts, ts, house_date_key)
                                    self.cursor.execute(sql_u, data_for_placehold)
                            else:
                                sql_i = "INSERT IGNORE INTO house_cals (house_date_key, house_id, cal_date, price, " \
                                        "booked, price_update_time, booked_update_time) " \
                                        "VALUES (%s, %s, %s, %s, %s, %s, %s)"

                                data_for_placehold = (house_date_key, house_id, hc['date'], price, booked, ts, ts)
                                self.cursor.execute(sql_i, data_for_placehold)
                    self.db.commit()
                except Exception as e:
                    self.logger.exception(e)
                    self.db.rollback()
                    update_calendar_response_sql = "UPDATE house_calendar_response SET parse_status=2 WHERE id=%s"
                    self.cursor.execute(update_calendar_response_sql, (r['id'],))
                    self.db.commit()
                else:
                    #TEST
                    delete_sql = "UPDATE house_calendar_response SET parse_status=1 WHERE id=%s"
                    # delete_sql = "DELETE house_calendar_response WHERE id=%s"
                    self.cursor.execute(delete_sql, (r['id'],))
                    self.db.commit()


if __name__ == "__main__":
    parser = CalendarParser()
    parser.run()