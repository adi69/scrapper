# -*- coding: utf-8 -*-
import scrapy
from scrape_zopper.items import Product, Merchant 

class ProductsSpider(scrapy.Spider):
    name = "zopper"
    allowed_domains = ["zopper.com"]
    start_urls = [ "http://stores.zopper.com/city/Gurgaon" ]

    def parse(self, response):
        #return scrapy.Request("http://stores.zopper.com/city/Gurgaon", 
        #    callback=self.parse_city_stores,
        #    meta = { 'city' : 'Gurgaon', 'count' : 0 }
        #)
        for link in response.xpath("//ul[@class='cities']/li"):
            url = link.xpath("a/@href").extract()[0]
            city = url.split('/')[-1]
            yield scrapy.Request(url, callback=self.parse_city_stores,
                meta = { 'city' : city, 'count' : 0 }
            )

    def parse_city_stores(self, response):
        
        #yield scrapy.Request('http://stores.zopper.com/sector-31-gurgaon/4803774854987776/catalog#contentTop', callback = self.parse_products,
        #    meta = {'other':True}
        #)
        
        for sel in response.xpath('//div[@itemtype="http://schema.org/ElectronicsStore"]'):
            response.meta['count'] += 1
            url = response.urljoin(sel.xpath('p[@class="websiteUrl"]/a[@class="brand-color-text"]/@href').extract()[0])
            
            merchant_link = '/'.join(url.split('/')[:-1])
            yield scrapy.Request(url, callback = self.parse_products,
                meta = {'other':True, 'merchant_link':merchant_link}
            )

        btn_load_more = response.xpath("//a[@class='brand-color-text btn-load-more']/@href")

        if btn_load_more:
            url = btn_load_more.extract()[0]
            yield scrapy.Request(url, callback = self.parse_city_stores,
                meta = { 'city': response.meta['city'], 'count' : response.meta['count'] }
            )

    def parse_products(self, response):
        btn_view_all = response.xpath('//div[@class="catalog-grid"]/a[@class="view-all brand-color-text large-screen-only"]/@href') 
        
        #yield scrapy.Request("http://stores.zopper.com/sector-14-gurgaon/4603882647846912/catalog/Mobiles%20and%20Tablets/Mobile%20Accessories", callback = self.parse_open_products)
        
        if btn_view_all.extract():
            for a in btn_view_all:
                url = response.urljoin(a.extract())
                yield scrapy.Request(url, callback = self.parse_open_products,
                    meta = {'merchant_link': response.meta['merchant_link']}
                )

        other_cats = response.xpath('//div[@class="other-sections-list"]/a[@class="pricat-link header-link header-link-bottom-lst brand-color-text"]')
        
        if response.meta['other'] and other_cats.extract():
            for cat in other_cats:
                url = response.urljoin(cat.xpath("@href").extract()[0])

                scrapy.Request(url, callback = self.parse_products,
                    meta = {'other':False}
                )

    def parse_open_products(self, response):
        for link in response.xpath('//div[@class="catalog-grid"]/div[@itemtype="http://schema.org/Product"]/*/h3[@class="product-name"]/a/@href'):
            url = response.urljoin(link.extract())
            print "OPEN PRODUCT =======> ", url
            yield scrapy.Request(url, callback = self.parse_product_real,
                meta = {'merchant_link': response.meta['merchant_link']}
            )

    def parse_product_real(self, response):
        item = Product()
        item['name'] = response.xpath('//h1[@id="popup-title"]/div/text()').extract()
        item['price'] = response.xpath('//span[@itemprop="price"]/text()').extract()
        item['link'] = response.url
        item['merchant_link'] = response.meta['merchant_link']
        
        specs = {}
        for tr in response.xpath('//table[@id="attribute-wrapper"]/tbody/tr'):
            specs[ tr.xpath('td[1]/text()').extract()[0] ] = tr.xpath('td[2]/text()').extract()[0]
        
        specs_str = ""
        for k,v in specs.items():
            specs_str += "%s: %s \n" % (k,v)
        item['specs'] = specs_str
        
        yield item
        print item
        

 
