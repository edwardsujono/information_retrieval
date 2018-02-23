from django.core.management.base import BaseCommand
from product.models import ShopeeProducts
import pysolr


class Command(BaseCommand):

    def handle(self, *args, **options):

        self.solr = pysolr.Solr('http://user_name:password@128.199.207.105:8983/solr/shopee_collection', timeout=10)

        self.start_indexing_amazon_products()
        self.start_indexing_lazada_products()
        self.start_indexing_shopee_products()
        return

    def start_indexing_shopee_products(self):

        all_products = ShopeeProducts.objects.all()
        list_product = []

        for product in all_products:
            list_product.append(product.get_serialize())

        self.solr.add(list_product)

        return

    def start_indexing_lazada_products(self):
        return

    def start_indexing_amazon_products(self):
        return
