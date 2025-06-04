import scrapy
from ..items import BookItem


class BookspiderSpider(scrapy.Spider):
    name            = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls      = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            book_page = book.css("h3 a::attr(href)").get()
            if book_page is not None:
                if "catalogue/" not in book_page:
                    book_page_url = f"https://books.toscrape.com/catalogue/{book_page}"
                else:
                    book_page_url = f"https://books.toscrape.com/{book_page}"
                yield response.follow(book_page_url, callback=self.parse_page)
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            if "catalogue/" not in next_page:
                next_page_url = f"https://books.toscrape.com/catalogue/{next_page}"
            else:
                next_page_url = f"https://books.toscrape.com/{next_page}"
            yield response.follow(next_page_url, callback=self.parse)
    
    def parse_page(self, response):
        bookitem = BookItem()
        
        bookitem["url"]               = response.url
        bookitem["title"]             = response.css('.product_main h1::text').get()
        bookitem["description"]       = response.css('#product_description + p::text').get()
        bookitem["category"]          = response.css('ul.breadcrumb > li:nth-child(3) > a::text').get()
        bookitem["upc"]               = response.xpath('//th[contains(text(), "UPC")]/following-sibling::td[1]/text()').get()
        bookitem["product_type"]      = response.xpath('//th[contains(text(), "Product Type")]/following-sibling::td[1]/text()').get()
        bookitem["price"]             = response.css('p.price_color::text').get()
        bookitem["price_excl_tax"]    = response.xpath('//th[contains(text(), "Price (excl. tax)")]/following-sibling::td[1]/text()').get()
        bookitem["price_incl_tax"]    = response.xpath('//th[contains(text(), "Price (incl. tax)")]/following-sibling::td[1]/text()').get()
        bookitem["tax"]               = response.xpath('//th[contains(text(), "Tax")]/following-sibling::td[1]/text()').get()
        bookitem["availability"]      = response.xpath('//th[contains(text(), "Availability")]/following-sibling::td[1]/text()').get()
        bookitem["number_of_reviews"] = response.xpath('//th[contains(text(), "Number of reviews")]/following-sibling::td[1]/text()').get()
        bookitem["rating"]            = response.xpath('//p[contains(@class, "star-rating")]/@class').get().split()[-1]
        
        yield bookitem
