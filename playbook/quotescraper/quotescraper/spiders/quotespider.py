import scrapy


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/js/"]

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            yield {
                "quote": quote.css('span.text::text').get(),
                "author": quote.css('small.author::text').get(),
                "tags": ", ".join([tag.get() for tag in quote.css('a.tag::text')])
            }
        next_page_url = "https://quotes.toscrape.com" + response.css('').get()
        if next_page_url is not None or next_page_url != "li.next a::attr(href)":
            response.follow(next_page_url, callback=self.parse)
