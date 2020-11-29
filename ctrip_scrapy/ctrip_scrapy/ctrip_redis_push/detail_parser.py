from parser import Parser
from pymysql.err import InterfaceError
import json

class DetailParser(Parser):
    def run(self):
        sql = "SELECT id, response FROM house_detail_response WHERE status=0 AND parse_status=0"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        data = []
        ids = []
        for r in rows:
            response = json.loads(r['response'])
            _result = response['result']
            a = json.loads(_result)
            b = a
            # TODO parse procedure
        try:
            self.db.commit()
        except InterfaceError as e:
            self.handle_db_timeout(sql, data, e)
        except Exception as e:
            self.logger.exception(e)
            self.db.rollback()
        else:
            pass
            # format_strings = ','.join(['%s'] * len(ids))
            # update_sql = "UPDATE house_detail_response SET parse_status=1 WHERE id IN (%s)" % format_strings
            # self.cursor.execute(update_sql, tuple(ids))
            # self.db.commit()

if __name__ == "__main__":
    parser = DetailParser()
    parser.run()