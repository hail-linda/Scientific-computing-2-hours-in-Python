# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from ctrip.items import HouseDetailItem, ListingItem, CalendarItem
from pymysql.err import InterfaceError

class CtripPipeline:
    def handle_db_timeout(self, spider, sql, params, e):
        """Reconnect db when db connection timeout."""
        spider.logger.info("database connection timeout, reconnect")
        spider.logger.exception(e)
        spider.db.ping(reconnect=True)
        spider.cursor.execute(sql, params)
        spider.db.commit()

    def process_item(self, item, spider):
        if item.__class__ == HouseDetailItem:
            sql = "INSERT IGNORE INTO house_detail_response (house_id, response, status) VALUES " \
                  "(%s, %s, %s)"
            params = (item['house_id'], item['response'], item['status'])

            sql_update = "UPDATE houses SET detail_crawled=1 WHERE house_id=%s"
            params_update = (item['house_id'],)
            try:
                spider.cursor.execute(sql, params)
                spider.cursor.execute(sql_update, params_update)
                spider.db.commit()
            except InterfaceError as e:
                self.handle_db_timeout(spider, sql, params, e)
            except Exception as e:
                spider.logger.exception(e)
                spider.db.rollback()
        elif item.__class__ == CalendarItem:
            sql = "INSERT IGNORE INTO house_calendar_response (house_id, response, status) VALUES " \
                  "(%s, %s, %s)"
            params = (item['house_id'], item['response'], item['status'])
            try:
                spider.cursor.execute(sql, params)
                spider.db.commit()
            except InterfaceError as e:
                self.handle_db_timeout(spider, sql, params, e)
            except Exception as e:
                spider.logger.exception(e)
                spider.db.rollback()
        elif item.__class__ == ListingItem:
            sql = "INSERT INTO house_list_response (response, city_id, page_index, page_size, price_range, status) " \
                  "VALUES (%s, %s, %s, %s, %s, %s)"
            params = (item['response'], item['city_id'], item['page_index'], item['page_size'],
                      item['price_range'], item['status'])
            try:
                spider.logger.info("Insert a listing response for city_id:%s, price_range:%s, page_index:%s" %
                                 (item['city_id'], item['price_range'], item['page_index']))
                spider.cursor.execute(sql, params)
                spider.db.commit()
            except InterfaceError as e:
                self.handle_db_timeout(spider, sql, params, e)
            except Exception as e:
                spider.logger.exception(e)
                spider.db.rollback()

        else:
            pass

        return item

    def open_spider(self, spider):
        spider.logger.debug("pipeline spider opend")

    def close_spider(self, spider):
        spider.logger.debug("pipline spider close")
