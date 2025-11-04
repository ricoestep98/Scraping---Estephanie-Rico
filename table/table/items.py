# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TableItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    idnum = scrapy.Field()
    firstname = scrapy.Field()
    lastname = scrapy.Field()
    username = scrapy.Field()
