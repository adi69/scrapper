import scrapy
from urls_list import urls
from flipkart_mobiles.items import Product
import json


class FkProductSpider(scrapy.Spider):
    name = 'FkProduct'
    allowed_domains = ['flipkart.com']
    start_urls = urls
    total = 0
    current_start = 1

    def parse(self, response):
        
        item = Product()
        product_basic = response.xpath('//*[@class="title"][@itemprop="name"]/text()').extract()[0]
        
        try:
            variant = response.xpath('//*[@class="subtitle"]/text()').extract()[0]
        except:
            variant = ''
        
        item['name'] = product_basic + ' ' + variant
        item['link'] = response.url
        
        try:
            item['rating'] = response.xpath('//*[@class="ratingHistogram"]/div/*[@class="bigStar"]/text()').extract()[0]
        except:
            item['rating'] = ''

        try:
            rating_string  = response.xpath(
                    '//*[@class="ratingHistogram"]/div/*[@class="subText"]/text()').extract()[1].\
                    encode('ascii', 'ignore').split()
            item['reviews_count'] = rating_string[2] 
        except:
            item['reviews_count'] = ''

        out_of_stock_class = response.xpath('//*[@class="out-of-stock-status"]')

        if out_of_stock_class:
            item['out_of_stock_status'] = 'Out of Stock'
            item['seller'] = ''
            item['selling_price'] = ''
            yield item
            return

        item['out_of_stock_status'] = '-'
        
        #Get Primary Seller:
        item['seller'] = response.xpath('//*[@class="seller-name"]/text()').extract()[0]
        dirty_price = response.xpath('//*[@class="selling-price omniture-field"]/text()').extract()[0]
        item['selling_price'] = filter(lambda x: x.isdigit(), dirty_price)
        yield item

        #Get Other Sellers:
        try:
            sellers=dict(json.loads(
                response.xpath('//*[@class="seller-table-wrap section"]/@data-config').extract()[0]))['dataModel']

            for seller in sellers:
                item['seller'] = seller['sellerInfo']['name']
                item['selling_price'] = seller['priceInfo']['sellingPrice']
                yield item
                print " more item ==================>>>>> "
                print item
        except:
            print "%s -------- single sellers only -----------------", item['name']
            
        
    def printf(self, File, data):
        with open(File, 'ab+') as f:
            f.write(data)


