import scrapy
from table.items import TableItem

class TablepracticeSpider(scrapy.Spider):
    name = "tablepractice"
    allowed_domains = ["webscraper.io"]
    start_urls = ["https://webscraper.io/test-sites/tables/tables-semantically-correct"]

    custom_settings = {
        'FEEDS': {
            'tabledata.json': {'format': 'json', 'overwrite': True}
        }
    }

    def parse(self, response):
        
        data = response.css('tbody tr')
        datalength = 0
        table_item = TableItem()

        for datas in data:

            table_item['idnum'] = datas.css('td:nth-child(1) ::text').get(),
            table_item['firstname'] = datas.css('td:nth-child(2) ::text').get(),
            table_item['lastname'] = datas.css('td:nth-child(3) ::text').get(),
            table_item['username'] = datas.css('td:nth-child(4) ::text').get(),

            yield table_item

