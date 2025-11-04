import scrapy
from quotesWithJsandScroll.items import QuoteswithjsandscrollItem
from scrapy_playwright.page import PageMethod

class QuotesjsandscrollSpider(scrapy.Spider):
    name = "quotesJsandScroll"

    custom_settings = {
        'FEEDS': {
            'qoutes.json': {'format': 'json', 'overwrite': True}
        }
    }

    def start_requests(self):
        url = 'http://quotes.toscrape.com/scroll'
        yield scrapy.Request(url, meta=dict(
            playwright = True,
            playwright_include_page = True,
            playwright_page_methods = [
                PageMethod('wait_for_selector','div.quote'),
                PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                PageMethod('wait_for_selector', 'div.quote:nth-child(11)') #10 per page
            ],
            errback = self.errback
        ))

    async def parse(self, response):
        page = response.meta['playwright_page']
        #screenshot = await page.screenshot(path="example.png", full_page = True) #to screenshot page
        await page.close()

        quote_item = QuoteswithjsandscrollItem()

        quotes = quotes = response.css('div.quote')
        
        for quote in quotes:
            quote_item['quote'] = quote.css('div.quote span ::text').get(),
            quote_item['author'] = quote.css('div.quote small ::text').get(),
            quote_item['tags'] = quote.css('div.tags a.tag ::text').extract(),

            yield quote_item

        next_page = response.css("nav li.next a ::attr(href)").get()
        if next_page is not None:
            next_page_url = 'http://quotes.toscrape.com' + next_page
            yield scrapy.Request(next_page_url, meta=dict(
                playwright = True,
                playwright_include_page = True,
                playwright_page_methods = [
                    PageMethod('wait_for_selector','div.quote')
                ],
                errback = self.errback
            ))

    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()