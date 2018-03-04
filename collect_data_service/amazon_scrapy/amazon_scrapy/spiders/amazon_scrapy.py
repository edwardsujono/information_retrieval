import scrapy
import re
import sys


class AmazonScrapy(scrapy.Spider):

    ###scraper name
    name = "AmazonScraper"

    ###choosing topic for crawl
    topic = input("choose topic: ")
    topic_link = topic.replace(" ","+")

    ###search amazon for the topic
    starting_link = "https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=" + topic_link
    start_urls = [starting_link]
    
    def parse_item(self,response):

        ###crawl detail page
        product_description = response.css("div #feature-bullets span.a-list-item::text").extract()
        price_whole = response.css("span#priceblock_ourprice::text").extract_first()
        original_price = response.css("div#unifiedPrice_feature_div span.a-text-strike::text").extract_first()
        product_name = response.css("span#productTitle::text").extract_first().strip()
        rating_temp = response.css("div#averageCustomerReviews i.a-icon-star span::text").extract_first()
        rating = rating_temp[:3]
        image_link = response.css("div#imgTagWrapperId img::attr(data-old-hires)").extract_first()
        self.stripper(product_description) ### stripping \n \t etc
        product_link = response.url
        comments = []
        
        for detail in response.css("div.review-data"):
            
            reviews =  detail.css("div.a-expander-content::text").extract_first()
            if(reviews):
                comments.append(reviews)
        
        

        ###if price or image link doesnt exist, throw away
        if(price_whole and image_link):
            yield{
                'product_description' : product_description,
                'product_name' : product_name,
                'current_price' : price_whole,
                'original_price' : original_price,
                'rating' : rating,
                'image_link' : image_link,
                'product_link' : product_link,
                'comments' : comments,

            }

    def parse(self,response):
        
        for detail in response.css("div.s-item-container"):
            
            ### link to item detail
            link = detail.css("a.s-access-detail-page::attr(href)").extract_first()

            if link is not None:
                try:
                    if "http" in link or "https" in link:
                        yield scrapy.Request(link, callback=self.parse_item)
                        print("success")
                except Exception:
                    print("error")

        next_page = response.css('a.pagnNext::attr(href)').extract_first()
        if next_page is not None:
            print ("next_page")
            next_page = response.urljoin(next_page)
            next_page = next_page
            yield scrapy.Request(next_page, callback=self.parse)

    def stripper(self,list_desc):
        for item in range(len(list_desc)):
            list_desc[item] = list_desc[item].strip()
