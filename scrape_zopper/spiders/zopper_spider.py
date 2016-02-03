# -*- coding: utf-8 -*-
import scrapy
from scrape_zopper.items import Product, Merchant 

class ZopperSpider(scrapy.Spider):
    name = "zopper"
    allowed_domains = ["zopper.com"]
    start_urls = [ "http://stores.zopper.com/city/Gurgaon" ]

    def parse(self, response):
        '''
            start parsing from here
        '''
        for link in response.xpath("//ul[@class='cities']/li"):
            url = link.xpath("a/@href").extract()[0]
            city = url.split('/')[-1]
            yield scrapy.Request(url, callback=self.parse_city_stores,
                meta = { 'city' : city, 'count' : 0 }
            )

    def parse_city_stores(self, response):
        '''
            get all the stores from a particular city
        '''
        for sel in response.xpath('//div[@itemtype="http://schema.org/ElectronicsStore"]'):
            a = "*/a[@class='theme-heading-text brand-color-hover']"
            merchant = Merchant()
            merchant['city'] = response.meta['city']
            merchant['name'] = str(sel.xpath(a + "/text()").extract()[0])
            merchant['link'] = str(response.urljoin(sel.xpath(a + "/@href").extract()[0]))
            merchant['address'] = self.get_address(sel)
            merchant['phone'] = sel.xpath('p[@class="phone"]/span/text()').extract()[0]
            response.meta['count'] += 1
            yield merchant
        
        btn_load_more = response.xpath("//a[@class='brand-color-text btn-load-more']/@href")

        if btn_load_more:
            url = btn_load_more.extract()[0]
            yield scrapy.Request(url, callback = self.parse_city_stores,
                meta = { 'city': merchant['city'], 'count' : response.meta['count'] }
            )

    def get_address(self, root):
        '''
            returns the address of a store on city page
        '''
        cityadd2 = root.xpath('p[@class="locality-city"]/text()').extract()[0]
        cityadd1 = root.xpath('p[@class="locality-city"]/a/text()').extract()[0]
        localadd = root.xpath('p[@class="address"]/a/span[@class="streetAddress"]/text()').extract()[0]
        return u' '.join((localadd, cityadd1, cityadd2)).encode('utf-8')
