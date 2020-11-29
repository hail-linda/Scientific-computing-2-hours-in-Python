from parser import Parser
from pymysql.err import InterfaceError
import json

class ListingParser(Parser):
    def run(self):
        page_num = 100
        while True:
            sql = "SELECT id, response FROM house_list_response WHERE status=0 AND parse_status=0 " \
                  "ORDER BY id asc LIMIT 0,%s"
            self.cursor.execute(sql, (page_num))
            rows = self.cursor.fetchall()
            print(len(rows))
            if len(rows) < 1:
                break

            data = []
            ids = []
            for r in rows:
                response = json.loads(r['response'])
                resp = json.loads(response['result'])

                items = resp['data']['items']
                if items is None:
                    self.logger.info("items is None, id is %s" % (r['id']))
                else:
                    for item in items:
                        data.append((item['unitId'], item['unitName'].encode("utf8"), item['productPrice'],
                                     item['cityId'], item['cityName'].encode("utf8")))
                ids.append(r['id'])

            sql = "INSERT IGNORE INTO houses (house_id, house_name, product_price, city_id, city_name) VALUES " \
                  "(%s, %s, %s, %s, %s)"
            try:
                self.cursor.executemany(sql, data)
                self.db.commit()
            except InterfaceError as e:
                self.handle_db_timeout(sql, data, e)
            except Exception as e:
                self.logger.exception(e)
                self.db.rollback()
            else:
                if len(ids) > 0:
                    format_strings = ','.join(['%s'] * len(ids))
                    update_sql = "UPDATE house_list_response SET parse_status=1 WHERE id IN (%s)" % format_strings
                    self.cursor.execute(update_sql, tuple(ids))
                    self.db.commit()

if __name__ == "__main__":
    parser = ListingParser()
    parser.run()