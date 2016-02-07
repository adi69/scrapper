# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    #category = scrapy.Field()
    merchant_link = scrapy.Field()
    specs = scrapy.Field()

class Merchant(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    open_time = scrapy.Field()
    city = scrapy.Field()
    #merchant_id = scrapy.Field()
    phone = scrapy.Field()
    link = scrapy.Field()
