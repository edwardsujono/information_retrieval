import scrapy
import urllib.request
import urllib.parse
import json
import csv
from scrapy_splash import SplashRequest

class ShopeeSpider(scrapy.Spider):
    NUM_OF_ITEMS = 30000
    name = "shopee"

    domain_url = "https://shopee.sg/"
    api_endpoints = {
            "category_list": "api/v1/category_list",
            "item_list": "api/v1/search_items",
            "item_detail": "api/v1/item_detail"
    }

    products = {}

    def shopee_api_request(self, request, params=None):
        url = self.domain_url + self.api_endpoints[request]
        if params is not None:
            url = url + "?" + urllib.parse.urlencode(params)

        return urllib.request.urlopen(url).read()

    def get_item_link(self, name, shop_id, item_id):
        quote = urllib.parse.quote(name)
        tmp = self.domain_url
        flag = False
        i = 0

        while i < len(quote):
            if quote[i] == "%":
                flag = True
                i += 2
            else:
                if flag:
                    tmp += "-"
                else:
                    tmp += quote[i]
                flag = False
                i += 1

        if not(tmp[-1] == '-'):
            tmp += '-'

        tmp += "i.{}.{}".format(shop_id, item_id)


        return tmp

    def get_image_link(self, image_id):
        return "https://cfshopeesg-a.akamaihd.net/file/" + image_id

    def get_category_list(self):
        return json.loads(self.shopee_api_request("category_list"))

    def get_item_list(self, item_list_params):
        return json.loads(self.shopee_api_request("item_list", item_list_params))["items"]

    def get_item_detail(self, item_id, shop_id):
        item_detail_params = {
                "item_id": item_id,
                "shop_id": shop_id
        }

        item_detail = json.loads(self.shopee_api_request("item_detail", item_detail_params))

        result = {}
        result["product_id"] = item_detail["itemid"]
        result["product_name"] = item_detail["name"]
        result["product_description"] = item_detail["description"]
        result["shop_id"] = item_detail["shopid"]
        result["product_link"] = self.get_item_link(item_detail["name"], item_detail["shopid"], item_detail["itemid"])
        result["rating"] = round(item_detail["rating_star"], 2)
        result["image_link"] = self.get_image_link(item_detail["image"])

        return result

    def start_requests(self):
        cat_list = self.get_category_list()

        for cat in cat_list:
            cat_id = cat['main']['catid']

            item_list_params = {
                    "by": "pop",
                    "order": "desc",
                    "newest": 0,
                    "limit": 50,
                    "categoryids": cat_id
            }

            item_list = self.get_item_list(item_list_params)

            for i in range(self.NUM_OF_ITEMS//len(cat_list)//50):
            # for i in range(1):
                # for j in range(4):
                #     item = item_list[j]
                for item in item_list:
                    item = item_list[j]
                    pid = str(item["itemid"]) + str(item["shopid"])
                    self.products[pid] = self.get_item_detail(item["itemid"], item["shopid"])
                    yield SplashRequest(self.products[pid]["product_link"], self.parse, endpoint="render.html", args={"wait": 10.0}, meta={'pid': pid})

                item_list_params["newest"] += item_list_params["limit"]
                item_list = self.get_item_list(item_list_params)

    def parse(self,response):
        pid = response.meta.get('pid')
        columns = ["product_id", "product_name", "original_price", "current_price", "product_description", "product_link", "rating", "image_link"]
        current_price_selector = 'span.shopee-product-info__header__price-before-discount__number::text'
        original_price_selector = 'div.shopee-product-info__header__real-price::text'
        
        current_price = response.css(current_price_selector).extract_first()
        original_price = response.css(original_price_selector).extract_first()
        
        self.products[pid]["current_price"] = current_price
        self.products[pid]["original_price"] = original_price

        tmp = {}

        for col in columns:
            if self.products[pid][col] is None:
                self.products[pid][col] = "-1"
                
            tmp[col] = self.products[pid][col]

        yield tmp
