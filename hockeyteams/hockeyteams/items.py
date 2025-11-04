# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HockeyteamsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    team_name = scrapy.Field()
    year = scrapy.Field()
    team_wins = scrapy.Field()
    team_losses = scrapy.Field()
    team_ot_losses = scrapy.Field()
    win_percentage = scrapy.Field()
    goals_for = scrapy.Field()
    goals_against = scrapy.Field()
    diff_success = scrapy.Field()

