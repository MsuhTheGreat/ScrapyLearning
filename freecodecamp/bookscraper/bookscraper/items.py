# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass


class BookItem(scrapy.Item):
    title             = scrapy.Field()
    description       = scrapy.Field()
    category          = scrapy.Field()
    price             = scrapy.Field()
    upc               = scrapy.Field()
    product_type      = scrapy.Field()
    price_excl_tax    = scrapy.Field()
    price_incl_tax    = scrapy.Field()
    tax               = scrapy.Field()
    availability      = scrapy.Field()
    number_of_reviews = scrapy.Field()
    rating            = scrapy.Field()
    url               = scrapy.Field()
    