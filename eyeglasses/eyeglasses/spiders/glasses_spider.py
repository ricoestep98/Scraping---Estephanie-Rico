import scrapy


class GlassesSpiderSpider(scrapy.Spider):
    name = "glasses_spider"
    allowed_domains = ["www.glassesshop.com"]
    start_urls = ["https://www.glassesshop.com/bestsellers"]

    custom_settings = {
        'FEEDS': {
            'glasses_shop.json': {'format': 'json', 'overwrite': True}
        }
    }

    def parse(self, response):
        
        products = response.xpath("//div[@class='row pt-lg-5 product-list column-1']/div[@class='col-12 col-lg-4 p-0']")

        for glasses in products:

            product_url = "https://www.glassesshop.com" + glasses.xpath(".//div/div[3]/div[2]/div/div[1]/div/a[1]/@href").get()
            product_img_link = glasses.css("div div.product-img-outer a:nth-child(4) img ::attr(data-src)").get()
            product_name = glasses.xpath(".//div/div[3]/div[2]/div/div[1]/div/a[1]/text()").get()
            product_price = glasses.xpath(".//div/div[3]/div[2]/div/div[2]/div/div[4]/span/span/text()").get()

            yield {
                'product_url': product_url,
                'product_image_link': product_img_link,
                'product_name': product_name,
                'product_price': product_price   
            }
            
        next_ppage = response.xpath("")

            
