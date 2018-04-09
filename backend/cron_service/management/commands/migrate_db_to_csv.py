from django.core.management.base import BaseCommand
from product.models import ShopeeProducts, LazadaProducts,\
    AmazonProducts, ProductName, ProductTokenCount
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
from common.utils import preprocess_all_token


class Command(BaseCommand):

    def handle(self, *args, **options):

        # this will build the indexer for the auto complete
        self.from_products_to_csv()
        return

    def from_products_to_csv(self):

        # all the word 2 vector operation will be done
        # in the analysis
        list_product = []
        list_product_id = []

        all_shopee_products = ShopeeProducts.objects.all()

        for shopee in all_shopee_products:

            list_product.append(preprocess_all_token(shopee.product_name))
            list_product_id.append(shopee.product_id)

        all_lazada_products = LazadaProducts.objects.all()

        for lazada in all_lazada_products:

            list_product.append(preprocess_all_token(lazada.product_name))
            list_product_id.append(lazada.product_id)

        all_amazon_products = AmazonProducts.objects.all()

        for amazon in all_amazon_products:

            list_product.append(preprocess_all_token(amazon.product_name))
            list_product_id.append(amazon.product_id)

        list_product = np.asarray(list_product)
        list_product_id = np.asarray(list_product_id)

        print(len(list_product))

        data = pd.concat([pd.DataFrame(list_product), pd.DataFrame(list_product_id)], axis=1)

        data.to_csv('list_product.csv')

    def from_products_to_product_id(self):

        list_product_id = []

        all_shopee_products = ShopeeProducts.objects.all()

        for shopee in all_shopee_products:
            list_product_id.append(shopee.product_id)

        all_lazada_products = LazadaProducts.objects.all()

        for lazada in all_lazada_products:
            list_product_id.append(lazada.product_id)

        all_amazon_products = AmazonProducts.objects.all()

        for amazon in all_amazon_products:
            list_product_id.append(amazon.product_id)

        list_product_id = np.asarray(list_product_id)

        np.savetxt("list_product_id.csv", list_product_id, delimiter=",", fmt="%s")
