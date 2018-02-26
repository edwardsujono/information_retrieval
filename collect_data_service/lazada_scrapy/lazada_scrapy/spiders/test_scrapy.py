import scrapy

##from scrapy.selector import Selector
##from scrapy.http import HtmlResponse


class LazadaCatSpider(scrapy.Spider):

    name = "LazCat"

    def start_requests(self):
        ## with open('laz_output.csv', 'rb') as csvfile:
        urls = [
            'https://www.lazada.sg/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
                
    def parse_item(self, response):
        
        ## filename = 'scrapy_test.csv'
        ## with open(filename, 'wb') as f:
        ##     f.write(response.body)
        
        product_name = response.css("h1.pdp-product-title::text").extract_first().strip()
        current_price = response.css("div.pdp-product-price > span::text").extract_first()
        original_price = response.css("div.pdp-product-price > div > span::text").extract_first()
        product_description = response.css("div.detail content > p > span::text").extract()
        rating = response.css("div.score > span::text").extract_first()
        image_link = response.css("div.gallery-preview-panel__content > img::attr(src)").extract()
        product_link = response.url

        if(current_price):
            yield{
                'product_desc' : product_description,
                'product_name' : product_name,
                'current_price' : current_price,
                'original_price' : original_price,
                'rating' : rating,
                'image_link' : image_link,
                'product_link' : product_link
            }
        
        ##self.log('Saved file %s' % filename)
        
            
    def parse(self, response):
        for item in response.css("li.lzd-site-menu-sub-item"):
            link = item.css('a::attr(href)').extract_first()
            cat_name = item.css("a > span::text").extract_first()
            for i in range(100):
                cat_url = "https:{}?page={}".format(link, i)
                yield scrapy.Request(url=cat_url, callback=self.parse_item)
                ##time.sleep(3)
            break

