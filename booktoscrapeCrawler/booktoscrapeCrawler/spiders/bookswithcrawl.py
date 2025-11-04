import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookswithcrawlSpider(CrawlSpider):
    name = "bookswithcrawl"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//li[@class='col-xs-6 col-sm-4 col-md-3 col-lg-3']/article/h3/a"), callback="parse_item", follow=True),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"))
    )

    custom_settings = {
        'FEEDS': {
            'books.json': {'format': 'json', 'overwrite': True}
        }
    }

    def parse_item(self, response):
        yield {
        'product_name': response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get(),
        'product_price': response.xpath("//div[@class='col-sm-6 product_main']/p/text()").get()
        }
