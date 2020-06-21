# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs
import pickle


class Themes(scrapy.Spider):
    name = 'themes'
    
    
    def start_requests(self):
        f = open("/home/hassan/Desktop/workspace/theme_crawler/sortedlinks.pickle","rb")
        data = pickle.load(f)
        f.close()
        urls = data
        for url in urls:
            yield scrapy.Request(url=url, callback=self.extract_url)

    def extract_url(self, response):

        theme_url = response.xpath("//h3[@class='_2WWZB']/a/@href").extract()
        l = response.url.replace("?view=list","").split("/category/")[1].split("/")
        category = l[0]
        subcategory= l[1]
        for e in theme_url:
            yield scrapy.Request(url=e, meta={'category':category,"subcategory":subcategory},callback=self.parse)


        url = response.xpath("//li[@class='pIPk0']/a/@href").extract()
        if(len(url)>0):
            url = list(set(url))
            for u in url:
                u = "https://themeforest.net"+u
                l1 = u.replace("?view=list","").split("/category/")[1].split("/")
                category = l1[0]
                subcategory= l1[1]
                yield scrapy.Request(url=u,callback=self.extract_theme)
        else:
            pass
    def extract_theme(self, response):
        l = response.url.replace("?view=list","").split("/category/")[1].split("/")
        category = l[0]
        subcategory= l[1]
        
        theme_url = response.xpath("//h3[@class='_2WWZB']/a/@href").extract()
        for e in theme_url:
            yield scrapy.Request(url=e, meta={'category':category,"subcategory":subcategory},callback=self.parse)
    
    def parse(self, response):
        print(response.url)
        name = response.xpath("//div[@class='item-header__title']/h1//text()").extract_first().strip()
        updated = response.xpath("//time[@class='updated']//text()").extract_first().strip()
        created = response.xpath("//td[@class='meta-attributes__attr-detail']/span//text()").extract_first().strip()
        url = response.url
        sales = response.xpath("//strong[@class='sidebar-stats__number']//text()").extract()[1].strip()
        tags = response.xpath("//span[@class='meta-attributes__attr-tags']/a//text()").extract()
        price = response.xpath("//span[@class='js-purchase-price']//text()").extract_first()
        yield{
            "name":name,
            "url":url,
            "updated":updated,
            "created":created,
            "sales":sales,
            "tags":tags,
            "price":price,
            "category":response.meta['category'],
            "subcategory":response.meta['subcategory']

        }



