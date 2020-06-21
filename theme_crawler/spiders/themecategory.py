# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs
import pickle


class ThemecategorySpider(scrapy.Spider):
    name = 'themecategory'
    
    
    def start_requests(self):
        f = open("/home/hassan/Desktop/workspace/theme_crawler/sortedlinks.pickle","rb")
        data = pickle.load(f)
        f.close()
        urls = data
        for url in urls:
            yield scrapy.Request(url=url, callback=self.extract_url)

    def extract_url(self, response):
        print(response.url)
        category = response.xpath("//a[@property='item']//text()").extract()
        box = response.xpath("//article[@class='_3Oe1A']").extract()

        for i in range(len(box)):
            soup = bs(box[i],'html.parser')
            price=""
            sales=""
            subcat=""
            sub_subcat=""
            try:
                price = soup.find('div',{'class':'-DeRq'}).text
            
            except:
                price = soup.find('span',{'class':'tf4fk'}).text
            
            try:
                sales = soup.find('div',{'class':'_3QV9M'}).text.replace(" Sales","")
            except:
                sales = "0"
            try:
                subcat = category[2]
            except:
                subcat = "None"

            a = response.url
            a = a[:a.find("?")][a.find("category"):].split("/")
            try:
                if (len(a)>=4):
                    sub_subcat = a[3]
                else:
                    sub_subcat = "None"
            except:
                sub_subcat = "None"
            yield{
                "url":soup.find('h3',{'class':'_2WWZB'}).find('a')['href'],
                "names":soup.find('h3',{'class':'_2WWZB'}).text,
                "category":category[1],
                "sub_category":subcat,
                "sub_sub_cat": sub_subcat,
                "price":price,
                "sales":sales,
                "tags":soup.find('span',{'class':'_3Q47d'}).text.replace('Tags: ',""),
                "last_updated":soup.find('span',{'class':'_3TIJT'}).text.strip()
            }




        url = response.xpath("//li[@class='pIPk0']/a/@href").extract()
        if(len(url)>0):
            url = list(set(url))
            yield scrapy.Request(url=response.url, callback=self.parse)
            for u in url:
                yield scrapy.Request(url="https://themeforest.net"+u, callback=self.parse)
        else:
            pass
            
                
    
    def parse(self, response):
        print(response.url)
        category = response.xpath("//a[@property='item']//text()").extract()
        box = response.xpath("//article[@class='_3Oe1A']").extract()

        for i in range(len(box)):
            soup = bs(box[i],'html.parser')
            price=""
            sales=""
            subcat=""
            sub_subcat=""
            # Price Section
            try:
                price = soup.find('div',{'class':'-DeRq'}).text
            
            except:
                price = soup.find('span',{'class':'tf4fk'}).text
            
            try:
                sales = soup.find('div',{'class':'_3QV9M'}).text.replace(" Sales","")
            except:
                sales = "0"
            try:
                subcat = category[2]
            except:
                subcat = "None"

            a = response.url
            a = a[:a.find("?")][a.find("category"):].split("/")
            try:
                if (len(a)>=4):
                    sub_subcat = a[3]
                else:
                    sub_subcat = "None"
            except:
                sub_subcat = "None"

            yield{
                "url":soup.find('h3',{'class':'_2WWZB'}).find('a')['href'],
                "names":soup.find('h3',{'class':'_2WWZB'}).text,
                "category":category[1],
                "sub_category":subcat,
                "sub_sub_cat": sub_subcat,
                "price":price,
                "sales":sales,
                "tags":soup.find('span',{'class':'_3Q47d'}).text.replace('Tags: ',""),
                "last_updated":soup.find('span',{'class':'_3TIJT'}).text.strip()
            }
        
        


