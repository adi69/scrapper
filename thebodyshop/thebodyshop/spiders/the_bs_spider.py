import scrapy
import json
from thebodyshop.items import Product
import urlparse #to extract PID from fk_url

class FkProductSpider(scrapy.Spider):
    name = 'bs'
    allowed_domains = ['www.thebodyshop.in']
    start_urls = [
            'http://www.thebodyshop.in/pages/Bath--Body-Care-Products---The-Body-Shop-India/pgid-367995.aspx',
            'http://www.thebodyshop.in/pages/Skin-Care-Products---The-Body-Shop-India/pgid-368151.aspx',
            'http://www.thebodyshop.in/pages/Hair-Care-Products---The-Body-Shop-India/pgid-368733.aspx',
            'http://www.thebodyshop.in/pages/Make-Up-Products---The-Body-Shop-India/pgid-368501.aspx',
            'http://www.thebodyshop.in/pages/Fragrance-Products---The-Body-Shop-India/pgid-368795.aspx',
            'http://www.thebodyshop.in/pages/Mens-Grooming-Products---The-Body-Shop-India/pgid-368675.aspx',
            'http://www.thebodyshop.in/pages/Beauty--Personal-Care-Accessories---The-Body-Shop-India/pgid-443919.aspx',
    ]

    def parse(self, response):
        '''
        Starts here. Requires two urls from `constants.py`
        1. `_start_urls`: starting urls list
        2. `self._lazy_load_api`: Loading more products pattern
        '''
        urls = response.xpath('//a[@class="mtc-a"]/@href').extract()
        
        for url in urls:
            yield scrapy.Request(url, callback = self.category)
        
    
    def category(self, response):
        '''
        Parse the flipkart product page
        Product: name, link, rating, reviews_count, seller, selling_price
        '''
        #for lazy loading
        for text in response.xpath('//script[@type="text/javascript"]').extract():
            pos = text.find('objShowCaseInputs')
            if pos > 0: 
                text = text[pos:]
                params = text[text.find('{') : text.find('}') + 1]
                print params
                break
            
        yield scrapy.Request(
                'http://www.thebodyshop.in/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput=' + params,
                callback = self.all_category_products,
                meta = {'params':params},
        )

    def all_category_products(self, response):
        #TODO: extract all product info here
        #names = response.xpath('//div[@class="bucket"]/div/h4[@class="mtb-title"]/text()').extract()
        #descs = response.xpath('//div[@class="bucket"]/div/div[@class="mtb-desc"]/text()').extract()
        #response.xpath('//div[@class="bucket"]/div/span[@class="mtb-price"]//node()[not(node())]').extract()
        if response.xpath('//div[@class="empty_msgsmall"]'):
            return

        product = Product()
        for item in response.xpath('//div[@class="bucket"]/div'):
            product['name'] = item.xpath('h4[@class="mtb-title"]/text()').extract()[0].strip()
            product['description'] = item.xpath('div[@class="mtb-desc"]/text()').extract()[0].strip()
            product['price'] = filter(lambda x: x.isdigit() ,''.join(item.xpath('span[@class="mtb-price"]//node()[not(node())]').extract()))
            product['link'] = item.xpath('a/@href').extract()
            yield product

        params = json.loads(response.meta['params'])
        params['PageNo'] += 1
        params = json.dumps(params)
        yield scrapy.Request(
                'http://www.thebodyshop.in/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput=' + params,
                callback = self.all_category_products,
                meta = {'params':params},
        )

