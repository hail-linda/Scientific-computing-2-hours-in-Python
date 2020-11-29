from parser import Parser
import json, csv


def write_csv_file(path, head, data):
    try:
        with open(path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, dialect='excel')

            if head is not None:
                writer.writerow(head)

            for row in data:
                writer.writerow(row)

    except Exception as e:
        print("Write an CSV file to path: %s, Case: %s" % (path, e))

class DetailParser(Parser):
    def run(self):
        p = 0
        max_p = 100000
        page_num = 10000
        data = []

        while p < max_p:
            offset = p * page_num
            sql = "SELECT hd.id, hd.house_id, hd.response, h.product_price FROM house_detail_response hd " \
                  "LEFT JOIN houses h ON hd.house_id=h.house_id " \
                  "WHERE hd.status=0 LIMIT %s,%s"
            self.cursor.execute(sql, (offset, page_num))
            rows = self.cursor.fetchall()
            print(p)
            if len(rows) == 0:
                break

            for r in rows:
                try:
                    response = json.loads(r['response'])
                    _result = response['result']
                    result = json.loads(_result)
                    lat = result['data']['unitDetail']['latitude']
                    lng = result['data']['unitDetail']['longitude']
                    city_id = result['data']['unitDetail']['cityId']
                    house_id = r['house_id']
                    price = r['product_price']
                    data.append([house_id, lat, lng, price, city_id])
                except Exception as e:
                    self.logger.exception(e)
            p = p + 1


        csv_file = "house_lnt_lng_price.csv"
        head = ['house_id', 'latitude', 'longitude', 'price', 'city_id']

        write_csv_file(csv_file, head, data)

if __name__ == "__main__":
    parser = DetailParser()
    parser.run()