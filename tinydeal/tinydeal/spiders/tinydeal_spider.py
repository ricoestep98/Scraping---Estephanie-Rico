import scrapy


class TinydealSpiderSpider(scrapy.Spider):
    name = "tinydeal_spider"
    allowed_domains = ["web.archive.org"]
    start_urls = ["https://web.archive.org/web/20161214180637/http://www.tinydeal.com/specials.html?page=3&disp_order=15"]

    custom_settings ={
        'FEEDS': {
            'productList.json': {'format': 'json', 'overwrite': True}
        }
    }

    def parse(self, response):
        
        products = response.xpath("//div[@class='p_box_wrapper']/li")

        for product in products:

            p_title = product.xpath(".//a[@class='p_box_title']/text()").get()
            p_url = product.xpath(".//a[@class='p_box_title']/@href").get()
            p_original_price = product.xpath(".//div[@class='p_box_price']/span[@class='normalprice fl']/text()").get()
            p_special_price = product.xpath(".//div[@class='p_box_price']/span[@class='productSpecialPrice fl']/text()").get()

            yield {
                'product_title': p_title,
                'product_link': p_url,
                'discounted_price': p_special_price,
                'Original_price': p_original_price
            }
        
        next_page = response.xpath("//div[@class='digg']/a[@class='nextPage']/@href").get()

        if next_page is not None:

            yield response.follow(next_page, callback=self.parse)

        
