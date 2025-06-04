import scrapy


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://chocolate.co.uk"]

    def parse(self, response):
        products = response.css('.product-item:not(.product-item--sold-out)')
        for product in products:
            url = product.css('.product-item__aspect-ratio').get()
            link_to_product = f"https://chocolate.co.uk/{url}"
            if link_to_product is not None or link_to_product != "":
                response.follow(link_to_product, callback=self.parse_product_page)

    def parse_product_page(self, response):
        yield {
            "url": response.url,
            "title": response.css('h1.product-meta__title::text').get(),
            "price": response.css('span.price--large::text').get(), # See Mullah Ji method
            "description_para_1": response.css('').get(),
            "description_para_2": response.css('').get(),
            "description_para_3": response.css('').get(),
            "ingredients": response.css('').get(),
            "allergens": response.css('').get()
        }
