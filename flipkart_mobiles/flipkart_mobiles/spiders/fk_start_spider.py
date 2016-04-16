import scrapy
import json
from flipkart_mobiles.items import Product


class FkProductSpider(scrapy.Spider):
    
    name = 'FkProduct'
    def __init__(self, url_pattern=''):
        self.name = 'fkp'
        self.allowed_domains = ['flipkart.com']
        self.start_urls = [url_pattern + '1', ]
        self._lazy_load_api = url_pattern
        
    current_start = 1
    total_urls = 0

    def parse(self, response):
        '''
        Starts here. Requires two urls from `constants.py`
        1. `_start_urls`: starting urls list
        2. `self._lazy_load_api`: Loading more products pattern
        '''
        items = response.xpath('//a[@data-tracking-id="prd_title"]') 
        
        for item in items:
            next_url = response.urljoin(item.xpath('@href').extract()[0])
            yield scrapy.Request(next_url, callback = self.parse_product)
        
        self.current_start += len(items)
        
        try:
            url = self._lazy_load_api + str(self.current_start)
            print '----> lazy url = %s' % url
            yield scrapy.Request(url, callback = self.parse)
            self.total_urls += 1
        except:
            print " ======> Error @%s: %s" % (response.url, Exception)
        
        print "--------> Lazy_Loads: %s (Products: %s)" %\
                (self.total_urls, self.current_start - 1)
        

    def parse_product(self, response):
        '''
        Parse the flipkart product page
        Product: name, link, rating, reviews_count, seller, selling_price
        '''
        item = Product()
        
        #Get Basic Name (Eg: `iphone 5s` in `iphone 5s (Silver, 32GB)`)
        product_basic = response.xpath(
            '//*[@class="title"][@itemprop="name"]/text()').extract()[0]
        
        #Try get Variant of the Product 
        try:
            variant = response.xpath('//*[@class="subtitle"]/text()').extract()[0]
        except:
            variant = ''
        
        item['name'] = product_basic + ' ' + variant
        item['link'] = response.url
        
        #Try get rating of the Product
        try:
            item['rating'] = response.xpath(
                '//*[@class="ratingHistogram"]/div/*[@class="bigStar"]/text()').\
                extract()[0]
        except:
            item['rating'] = ''
        
        #Try get total reviews (for popularity of product)
        try:
            rating_string  = response.xpath(
                    '//*[@class="ratingHistogram"]/div/*[@class="subText"]/text()').\
                    extract()[1].encode('ascii', 'ignore').split()
            item['reviews_count'] = rating_string[2] 
        except:
            item['reviews_count'] = ''
        
        #Try get List Price
        try:
            item['list_price'] = response.xpath(
                    '//*[@class="price"]/text()').extract()[0]
        except:
            item['list_price'] = ''

        out_of_stock_class = response.xpath('//*[@class="out-of-stock-status"]')

        if out_of_stock_class:
            item['out_of_stock_status'] = 'Out_of_Stock'
            item['seller'] = ''
            item['selling_price'] = ''
            yield item
            return

        item['out_of_stock_status'] = ''
        
        #Get Primary Seller:
        item['seller'] = response.xpath(
            '//*[@class="seller-name"]/text()').extract()[0]
        dirty_price = response.xpath(
            '//*[@class="selling-price omniture-field"]/text()').extract()[0]
        item['selling_price'] = filter(lambda x: x.isdigit(), dirty_price)
        yield item

        #Get Other Sellers:
        try:
            sellers=dict(json.loads(
                response.xpath(
                    '//*[@class="seller-table-wrap section"]/@data-config').\
                    extract()[0]))['dataModel']

            for seller in sellers:
                item['seller'] = seller['sellerInfo']['name']
                item['selling_price'] = seller['priceInfo']['sellingPrice']
                yield item
        except:
            print "%s -------- Single seller only: ", item['name']
            

