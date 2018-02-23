import scrapy
import re
import sys


class AmazonScrapy(scrapy.Spider):

    name = "AmazonScraper"
        
    start_urls = ["https://www.amazon.com/b/ref=s9_acss_bw_cg_BeautCat_3b1_w?_encoding=UTF8&node=6684060011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=X0EDCWWBMEV5ZA9K24TB&pf_rd_t=101&pf_rd_p=255859a7-f959-5ef3-85fe-df1e2c3daad9&pf_rd_i=6682399011"]
    
    def parse_item(self,response):

        product_description = response.css("div #feature-bullets span.a-list-item::text").extract()
        price_whole = response.css("span#priceblock_ourprice::text").extract()
        original_price = response.css("div#unifiedPrice_feature_div span.a-text-strike::text").extract_first()
        product_name = response.css("span#productTitle::text").extract_first().strip()
        rating_temp = response.css("div#averageCustomerReviews i.a-icon-star span::text").extract_first()
        rating = rating_temp[:3]
        image_link = response.css("div#imgTagWrapperId img::attr(src)").extract()
        self.stripper(product_description)
        product_link = response.url

        yield{
            'product_desc' : product_description,
            'product_name' : product_name,
            'current_price' : price_whole,
            'original_price' : original_price,
            'rating' : rating,
            'image_link' : image_link,
            'product_link' : product_link

        }

    def parse(self,response):
        for detail in response.css("div.s-item-container"):
            
            link = detail.css("a.s-access-detail-page::attr(href)").extract_first()
            if link is not None:
                yield scrapy.Request(link,callback=self.parse_item)


            yield {
            #     'product_id' : product_id,
            #     'product_name'  : detail.css("h2.s-access-title::text").extract_first(),
            #     'original_price' : detail.css("span.a-size-base-plus::text").extract_first(),
            #     'current_price' : price,
                'product_link' : link,
            #     'rating' : rating,
            #     'image_link' : detail.css("img::attr(src)").extract_first()

            }

        next_page = response.css('a.pagnNext::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def stripper(self,list_desc):
        for item in range(len(list_desc)):
            list_desc[item] = list_desc[item].strip()
