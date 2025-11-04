import scrapy
from countryscraper.items import CountryscraperItem


class CountrySpider(scrapy.Spider):
    name = "country"
    allowed_domains = ["www.scrapethissite.com"]
    start_urls = ["https://www.scrapethissite.com/pages/simple/"]

    custom_settings = {
        'FEEDS': {
        'countries.json': {'format': 'json', 'overwrite': True},
        }
    }

    def parse(self, response):
        country_item = CountryscraperItem()
        countries = response.css('div.col-md-4.country')

        for country in countries:
            
            country_item['country_name'] = country.css('h3.country-name').xpath('normalize-space(./i/following-sibling::text())').get(),
            country_item['capital'] = country.css('div.country-info span.country-capital::text').get(),
            country_item['population'] = country.css('div.country-info span.country-population::text').get(),
            country_item['area_in_km'] = country.css('div.country-info span.country-area::text').get(),
            
            yield country_item
