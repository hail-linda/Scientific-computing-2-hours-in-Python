# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AirbnbspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class listItem(scrapy.Item):
    price = scrapy.Field()
    description = scrapy.Field()
    house_id = scrapy.Field()
    map_id = scrapy.Field()
    response = scrapy.Field()

class calendarItem(scrapy.Item):
    house_id = scrapy.Field()
    response = scrapy.Field()

