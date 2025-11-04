# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EcommercestaticItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    product_category = scrapy.Field() 
    product_link = scrapy.Field()
    product_description = scrapy.Field()
    product_price = scrapy.Field()
    product_reviews = scrapy.Field()
    product_star_rating = scrapy.Field()
