# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    
    name = scrapy.Field()
    link = scrapy.Field()
    rating = scrapy.Field()
    reviews_count = scrapy.Field()
    out_of_stock_status = scrapy.Field()
    seller = scrapy.Field()
    selling_price = scrapy.Field()

