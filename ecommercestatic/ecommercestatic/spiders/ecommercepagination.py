import scrapy
from ecommercestatic.items import EcommercestaticItem


class EcommercepaginationSpider(scrapy.Spider):
    name = "ecommercepagination"
    allowed_domains = ["webscraper.io"]
    start_urls = ["https://webscraper.io/test-sites/e-commerce/static"]

    custom_settings = {
        'FEEDS': {
            'output.json': {'format': 'json', 'overwrite': True}
        }
    }

    def parse(self, response):
        computer_categories = ['laptops', 'tablets']
        phone_categories = ['touch']

        for computer_category in computer_categories:
            url = 'https://webscraper.io/test-sites/e-commerce/static/computers/'
            next_url = url + computer_category
            yield response.follow(next_url, callback = self.parse_computers, meta = {'computer_category': computer_category})
        print("*********** done **********")
        
        for phone_category in phone_categories:
            url = 'https://webscraper.io/test-sites/e-commerce/static/phones/'
            next_url = url + phone_category
            print("***********")
            print(next_url)
            yield response.follow(next_url, callback = self.parse_phones, meta = {'phone_category': phone_category})

    def parse_computers(self, response):
        category = response.meta['computer_category']        
         
        product_list = response.css('div.col-md-4.col-xl-4')

        for product in product_list:

            product_link = 'https://webscraper.io' + product.css('div.caption h4 a::attr(href)').get()
            yield response.follow(product_link, callback = self.parse_product, meta = {'product_category': category, 'product_link': product_link})

        next_button = response.xpath('//*[@id="static-pagination"]/nav/ul/li/a[@rel="next"]/@href').get()
        next_page = 'https://webscraper.io' + next_button

        if next_page is not None:
            yield response.follow(next_page, callback = self.parse_computers, meta = {'computer_category': category})

    def parse_phones(self, response):
        category = response.meta['phone_category']        
         
        product_list = response.css('div.col-md-4.col-xl-4')

        for product in product_list:

            product_link = 'https://webscraper.io' + product.css('div.caption h4 a::attr(href)').get()
            yield response.follow(product_link, callback = self.parse_product, meta = {'product_category': category, 'product_link': product_link})

        next_button = response.xpath('//*[@id="static-pagination"]/nav/ul/li/a[@rel="next"]/@href').get()
        next_page = 'https://webscraper.io' + next_button

        if next_page is not None:
            yield response.follow(next_page, callback = self.parse_phones, meta = {'phone_category': category})

    def parse_product(self, response):
        category = response.meta['product_category']
        product_item = EcommercestaticItem()

        rating = response.css('div.ratings p span')

        product_item['product_name'] = response.css('div.caption h4.card-title.title ::text').get(),
        product_item['product_category'] = category,
        product_item['product_link'] = response.meta['product_link'],
        product_item['product_description'] = response.css('div.caption p.description.card-text ::text').get(),
        product_item['product_price'] = response.css('div.caption h4.float-end.price ::text').get(),
        product_item['product_reviews'] = response.css('p.review-count').xpath('normalize-space(text())').get(),
        product_item['product_star_rating'] = len(rating),

        yield product_item
