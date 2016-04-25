import scrapy
import json
from BB.items import Product
from cookies import cookie
from scrapy.shell import inspect_response #inspect_response(response, self)


class BBSpider(scrapy.Spider):
 
    name = 'bbspider'
    allowed_domains = ['bigbasket.com']
    start_urls = ['http://www.bigbasket.com']
    i = 1

    def __init__(self, city):
        self.biscuit = cookie[city]
    
    def parse(self, response):
        print '-------------------- i = ', self.i
        yield scrapy.Request(
            url="http://www.bigbasket.com/product/page/%s/?sid=HbqW8YeibWQDoWMSomNjozQ4OaJhb8KibHTNAdaibmbDomRzojE3"%self.i,
            cookies=self.biscuit, callback=self.product_page)
        self.i += 1
    
    def product_pagex(self, response):
        item = Product()
        products = response.xpath('//*[contains(@id, "product")]')
        d_ = {}
        
        if not products: 
            print "---- THAT'S ALL FOLKS ---- ", response.url 
            return

        for product in products:
            
            try:
                link = product.xpath(
                    'descendant::*[@class="uiv2-title-tool-tip"]/a/@href').\
                    extract()[0]
            except:
                link = ''

            # to not repeat the products
            if link in d_:
                continue
            else:
                d_[link] = True

            try:
                name = product.xpath(
                    'descendant::*[@class="uiv2-title-tool-tip"]/a/text()').\
                    extract()[0].strip()
            except:
                name = ''
            
            p_v_tag = product.xpath(
                'descendant::*[@class="uiv2-field-wrap mt10"]/select/option[@selected and not(@disabled)]/text()').extract()
            
            try:
                price = p_v_tag[1].strip()
            except:
                price = ''
            
            try:
                variant = p_v_tag[0].strip()
            except:
                variant = ''
            
            item['link'] = response.urljoin(link)
            item['price'] = price
            item['name'] = name + ', ' + variant 
            yield item
        
        yield scrapy.Request(
            url="http://www.bigbasket.com/product/page/%s/?sid=HbqW8YeibWQDoWMSomNjozQ4OaJhb8KibHTNAdaibmbDomRzojE3"%self.i,
            cookies=self.biscuit, callback=self.product_page)
        self.i += 1

    def product_page(self, response):
        urls = response.xpath('//*[@class="uiv2-title-tool-tip"]/a/@href').extract()
        print urls
        if not urls: print "--------DONE:OVER&OUT--------"; return
        
        for item in urls:
            yield scrapy.Request(url=response.urljoin(item),
                    cookies=self.biscuit, callback=self.product)
        
        yield scrapy.Request(
            url="http://www.bigbasket.com/product/page/%s/?sid=HbqW8YeibWQDoWMSomNjozQ4OaJhb8KibHTNAdaibmbDomRzojE3"%self.i,
            cookies=self.biscuit, callback=self.product_page)
        self.i += 1

    def product(self, response):
        item = Product()
        
        product_area = response.xpath(
                '//div[@class="pd-right-col uiv2-product-info-wrapper uiv2-mar-t-15"]')
        count = 0
        name = ''
        price = ''

        for product in product_area:
            if not product.xpath('@style["display:none;"]'):
                count += 1
                if count > 1: 
                    name = '' 
                    price = '' 
                    break
                name = product.xpath(
                        'descendant::*[@class="uiv2-product-name"]/h1/text()').extract()[0]
                price = product.xpath(
                        'descendant::*[@class="uiv2-price"]/text()').extract()[0]
        
        if count > 1:
            for product in product_area:
                if product.xpath('//*[@class="uiv2-size-variants"]/input[@checked]'):
                    name = product.xpath(
                            'descendant::*[@class="uiv2-product-name"]/h1/text()').extract()[0]
                    price = product.xpath(
                            'descendant::*[@class="uiv2-price"]/text()').extract()[0]
                    break

        item['name'] = name.strip()
        item['price'] = price.strip()
        item['link'] = response.url

        yield item
