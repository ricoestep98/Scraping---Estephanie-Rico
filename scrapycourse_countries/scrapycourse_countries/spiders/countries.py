import scrapy


class CountriesSpider(scrapy.Spider):
    name = "countries"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    custom_settings = {
        'FEEDS': {
            'countries_course.json': {'format': 'json', 'overwrite': True}
        }
    }
    def parse(self, response):
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = 'https://www.worldometers.info/' + country.xpath(".//@href").get()

            #FOLLOWING LINK

            #absolute_url = f"https://www.worldometers.info{link}"
            #absolute_url = response.urljoin(link) #its like fetch command in scrapy shell

            #yield scrapy.Request(url=absolute_url) or you can do below
            
            yield response.follow(url = link, callback=self.parse_country, meta={'country_name': name, 'link': link})

    def parse_country(self, response):
        r = response.xpath('//div[@class="not-prose"]')[0]
        rows = r.xpath('.//table/tbody/tr')

        country_name = response.meta['country_name']
        country_link = response.meta['link']

        for row in rows:

            year = row.xpath(".//td/text()")[0].get()
            population = row.xpath(".//td/text()")[1].get()

            yield {
                'country_name': country_name,
                'link': country_link,
                'year': year,
                'population': population
            }

 