# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
class CtripItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class HouseDetailItem(scrapy.Item):
    house_id = scrapy.Field()
    response = scrapy.Field()
    status = scrapy.Field()


class CalendarItem(scrapy.Item):
    response = scrapy.Field()
    house_id = scrapy.Field()
    status = scrapy.Field()


class ListingItem(scrapy.Item):
    response = scrapy.Field()
    city_id = scrapy.Field()
    page_index = scrapy.Field()
    page_size = scrapy.Field()
    price_range = scrapy.Field()
    status = scrapy.Field()


