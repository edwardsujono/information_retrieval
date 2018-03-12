import scrapy
import urllib.request
import urllib.parse
import json
import csv
from scrapy_splash import SplashRequest


##from scrapy.selector import Selector
##from scrapy.http import HtmlResponse


class LazadaCatSpider(scrapy.Spider):
    NUM_OF_ITEMS = 30000
    name = "LazCat"

    def start_requests(self):
        ## with open('laz_output.csv', 'rb') as csvfile:
        urls = [
            'https://www.lazada.sg/'
        ]
        for url in urls:
            yield SplashRequest(url=url, callback=self.parse)

    def parse_item(self, response):

        ## filename = 'scrapy_test.csv'
        ## with open(filename, 'wb') as f:
        ##     f.write(response.body)

        product_name = response.css("h1.pdp-product-title::text").extract_first()
        current_price = response.css("div.pdp-product-price > span::text").extract_first()
        original_price = response.css("div.pdp-product-price > div > span::text").extract_first()
        product_description = response.css("div.pdp-product-hightlights > ul > li::text").extract()
        rating = response.css("div.score > span::text").extract_first()
        image_link = response.css("div.gallery-preview-panel__content > img::attr(src)").extract()
        product_link = response.url
        product_comment = response.css("div.mod-reviews > div.item > div.content::text").extract()

        if (current_price):
            yield {
                'product_id': product_link,
                'product_description': product_description,
                'product_name': product_name,
                'current_price': current_price,
                'original_price': original_price,
                'rating': rating,
                'image_link': image_link,
                'çomments': product_comment
            }

            ##self.log('Saved file %s' % filename)

    def parse(self, response):
        for item in response.css("li.lzd-site-menu-sub-item"):
            link = item.css('a::attr(href)').extract_first()
            cat_name = item.css("a > span::text").extract_first()
            for i in range(1):
                try:
                    cat_url = "https:{}?page={}".format(link, i)
                    yield SplashRequest(url=cat_url, callback=self.parse_itempage)
                except Exception:
                    print ("error parse first")

    def parse_itempage(self, response):

        ### link to item detail
        links = response.css("div.cRjKsc > a::attr(href)").extract()

        if len(links) > 0:
            try:
                for link in links:
                    update_link = "http:" + link
                    yield SplashRequest(url=update_link, callback=self.parse_item)
                    return
            except Exception:
                print("error parse second")

                # next_page = response.css('a.pagnNext::attr(href)').extract_first()
                # if next_page is not None:
                #     print ("next_page")
                #     next_page = response.urljoin(next_page)
                #     next_page = next_page
                #     yield SplashRequest(next_page, callback=self.parse)

