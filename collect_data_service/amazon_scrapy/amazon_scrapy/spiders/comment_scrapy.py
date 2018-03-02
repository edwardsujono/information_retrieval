import scrapy
import re
import sys
import os
import json
from pprint import pprint


class AmazonScrapy(scrapy.Spider):

    ###scraper name
    name = "AmazonCommentScraper"

    

    def start_requests(self):
        print("loading...")
        list_link = []
        
        data = json.load(open('D:/Academic/Sem 8/information_retrieval/collect_data_service/amazon_scrapy/output.json',mode='r',encoding='UTF-8'))
        for i in range(0,len(data)):
            list_link.append(re.sub(r'\/ref=.*','',data[i]["product_link"],flags=re.DOTALL))
        print("load data done..")

        ###index for partial scrapping
        start_index = int(input("choose start index: "))
        end_index = int(input("choose end index: "))
        ###setting up requests
        urls = list_link[start_index:end_index]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)
    

    def parse(self,response):
        comments = []
        link = response.url
        for detail in response.css("div.review-data"):
            
            reviews =  detail.css("div.a-expander-content::text").extract_first()
            if(reviews):
                comments.append(reviews)
        
        yield{
            'link_item' : link,
            'comments' : comments 
        }

    def stripper(self,list_desc):
        for item in range(len(list_desc)):
            list_desc[item] = list_desc[item].strip()

             

