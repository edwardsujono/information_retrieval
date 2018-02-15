from django.core.management.base import BaseCommand
from backend.product.models import AmazonProducts, LazadaProducts, ShopeeProducts
import pysolr


class Command(BaseCommand):

    def handle(self, *args, **options):
        return

    def start_indexing_shopee_products(self):
        return

    def start_indexing_lazada_products(self):
        return

    def start_indexing_amazon_products(self):
        return
