import scrapy
from ..items import QuotescraperItem


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            quote_scraper_item = QuotescraperItem()
            quote_scraper_item['quote'] = quote.css('span.text::text').get()
            quote_scraper_item['author'] = quote.css('small.author::text').get()
            quote_scraper_item['tags'] = quote.css('a.tag::text').getall()
            yield quote_scraper_item
        
