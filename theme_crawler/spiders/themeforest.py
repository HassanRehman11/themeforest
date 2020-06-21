# -*- coding: utf-8 -*-
import scrapy


class ThemeforestSpider(scrapy.Spider):
    name = 'themeforest'
    start_urls = ['https://themeforest.net/category']
    URL = 'https://themeforest.net'

    def parse(self, response):
        sub_data = []
        categories = response.xpath("//div[@class='category-section']/ul[@class='first']/li")
        for c in categories:
            category_name = c.xpath("a//text()").extract_first()
            url = c.xpath("a/@href").extract_first()
            record = c.xpath("small//text()").extract_first()
            sub_cat = c.xpath("ul/li")
            
            for s in sub_cat:
                rec = s.xpath("small//text()").extract_first()
                sub_data.append(
                    {
                        "sub_name":s.xpath("a//text()").extract_first(),
                        "url":s.xpath("a/@href").extract_first(),
                        "record": int(rec.replace(')','').replace('(',''))
                    }
                )
            yield{
                "category_name":category_name,
                "url":url,
                "record":int(record.replace(')','').replace('(','')),
                "subcategory":sub_data
            }
       