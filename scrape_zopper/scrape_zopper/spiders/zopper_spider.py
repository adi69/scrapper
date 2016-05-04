# -*- coding: utf-8 -*-
import scrapy
from scrape_zopper.items import Product, Merchant 

class ZopperSpider(scrapy.Spider):
    '''
        get zopper merchants list
    '''
    name = "merchant"
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
            
            yield scrapy.Request(merchant['link'], callback = self.parse_store,
                meta = { 'merchant': merchant, 'count' : response.meta['count'] }
            )
        
        btn_load_more = response.xpath("//a[@class='brand-color-text btn-load-more']/@href")

        if btn_load_more:
            url = btn_load_more.extract()[0]
            yield scrapy.Request(url, callback = self.parse_city_stores,
                meta = { 'city': merchant['city'], 'count' : response.meta['count'] }
            )
    
    def parse_store(self, response):
        '''
            profile page of a store
        '''
        merchant = response.meta['merchant']
        operations = response.xpath('//*[@id="hoop"]/table/tbody/tr')
        
        hrs_of_op = {}
        for tr in operations:
            day = tr.xpath('td[1]/text()').extract()[0]
            hrs = tr.xpath('td[2]/div/text()').extract()[0]
            hrs_of_op[day] = hrs
        
        hrs_of_op_str = ""
        for k,v in hrs_of_op.items():
            hrs_of_op_str += "%s: %s \n" % (k,v)
        merchant['open_time'] = hrs_of_op_str
        
        url = response.urljoin(response.xpath('/html/body/div[1]/div[2]/ul[1]/li[4]/a/@href').extract()[0])
        yield scrapy.Request(url, callback = self.parse_store_map,
            meta = { 'merchant': merchant }
        )
        
    def parse_store_map(self, response):
        '''
            store on map
        '''
        merchant = response.meta['merchant']

        map_script_data = response.xpath('/html/body/script[2]/text()').extract()[0]
        merchant['longitude'] = self.get_long_lat("longitude", map_script_data)
        merchant['latitude'] = self.get_long_lat("latitude", map_script_data)
        yield merchant

    def get_long_lat(self, s, data):
        '''
            return latitude longitude of store
        '''
        data_ = data.split(',') 
        for i in data_:
            if i.find(s) != -1:
                lat = i.split(':')[1].strip().strip('"')
                return lat
        return -1

    def get_address(self, root):
        '''
            returns the address of a store on city page
        '''
        cityadd2 = root.xpath('p[@class="locality-city"]/text()').extract()[0]
        cityadd1 = root.xpath('p[@class="locality-city"]/a/text()').extract()[0]
        localadd = root.xpath('p[@class="address"]/a/span[@class="streetAddress"]/text()').extract()[0]
        return u' '.join((localadd, cityadd1, cityadd2)).encode('utf-8')
