import scrapy
from ..items import QuoteItem
from scrapy_playwright.page import PageMethod


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
    # allowed_domains = ["quotes.toscrape.com"]
    # start_urls = ["https://quotes.toscrape.com/js/"]

    def start_requests(self):
        url = "https://quotes.toscrape.com/js/"
        yield scrapy.Request(url, meta=dict(
            playwright = True,
            playwright_include_page = True,
            playwright_page_methods = [
                PageMethod('wait_for-selector', 'div.quote')
            ],
            errback = self.errback
        ))

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            quote_item = QuoteItem()
            quote_item["quote"] = quote.css('span.text::text').get()
            quote_item["author"] = quote.css('small.author::text').get()
            quote_item["tags"] = ", ".join([tag.get() for tag in quote.css('a.tag::text')])
            yield quote_item

        next_page_url = response.css('li.next a::attr(href)').get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse, meta={'playwright': True})

    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()