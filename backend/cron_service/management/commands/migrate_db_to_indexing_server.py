from django.core.management.base import BaseCommand
from product.models import ShopeeProducts, LazadaProducts,\
    AmazonProducts, ProductName, ProductTokenCount
from nltk.corpus import stopwords


class Command(BaseCommand):

    def handle(self, *args, **options):

        # this will build the indexer for the auto complete
        self.start_save_to_product_name_db()
        return

    def start_save_to_product_name_db(self):

        # collect all the product name
        # all_shopee = ShopeeProducts.objects.all()
        # all_lazada = LazadaProducts.objects.all()
        # all_amazon = AmazonProducts.objects.all()
        #
        # for shopee in all_shopee:
        #
        #     product_name = ProductName(
        #         product_link=shopee.product_link,
        #         product_name=shopee.product_name
        #     )
        #
        #     product_name.save()
        #
        # for lazada in all_lazada:
        #
        #     product_name = ProductName(
        #         product_link=lazada.product_link,
        #         product_name=lazada.product_name
        #     )
        #
        #     product_name.save()
        #
        # for amazon in all_amazon:
        #
        #     product_name = ProductName(
        #         product_link=amazon.product_link,
        #         product_name=amazon.product_name
        #     )
        #
        #     product_name.save()

        all_products = ProductName.objects.all()
        dictionary_save = {}

        for product in all_products:

            list_product_token = product.product_name.split(" ")

            for product_token in list_product_token:

                if dictionary_save.get(product_token) is None:
                    dictionary_save[product_token] = 0

                dictionary_save[product_token] += 1

        for key, value in dictionary_save.items():

            product_token_count = ProductTokenCount(
                token_name=key,
                token_count=value
            )
            product_token_count.save()

    def removing_stopword(self, product_name):

        word_list = product_name.split(" ")
        filtered_words = [word for word in word_list if word not in stopwords.words('english')]

        return_product_name = ""

        for word in filtered_words:
            return_product_name += word + " "

        return return_product_name[:len(return_product_name)-1]
