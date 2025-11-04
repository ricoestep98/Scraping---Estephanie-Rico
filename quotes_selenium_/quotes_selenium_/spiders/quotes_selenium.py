import scrapy
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector

class QuotesSeleniumSpider(scrapy.Spider):
    name = "quotes_selenium"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/js/"]

    def __init__(self):
        chrome_option = Options()
        chrome_option.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_option)
        driver.set_window_size(1020,1080)
        driver.get("https://quotes.toscrape.com/js/")
        
        #get pagesource for all pages
        #get link
        #follow link
        #get page source
        self.html = driver.page_source
        driver.close()

    custom_settings = {
            'FEEDS': {
                'quotes.json': {'format': 'json', 'overwrite': True}
            }
        }
    
    def parse(self, response):
        resp = Selector(text=self.html)

        for quotes in resp.xpath("//div[@class='quote']"):
            yield{
                'Quote': quotes.xpath(".//span[@class='text']/text()").get(),
                'Author': quotes.xpath(".//span/small/text()").get(),
                'Tags': quotes.xpath(".//div[@class='tags']/a/text()").extract()
            }
            

        next_page = response.xpath("//nav/ul/li[@class='next']/a/@href").get()
        print(next_page)
        if next_page:
            chrome_option = Options()
            chrome_option.add_argument("--headless")

            driver = webdriver.Chrome(options=chrome_option)
            driver.set_window_size(1020,1080)
            driver.get('https://quotes.toscrape.com' + next_page)
            self.html = driver.page_source
            

            yield response.follow(url='https://quotes.toscrape.com'+next_page, callback=self.parse)
        else:
            print("Not found")