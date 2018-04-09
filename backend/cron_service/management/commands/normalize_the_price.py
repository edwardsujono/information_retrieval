from django.core.management.base import BaseCommand
from product.models import AmazonProducts, LazadaProducts, ShopeeProducts
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **options):

        # this will build the indexer for the auto complete
        self.normalize_products(ShopeeProducts)
        self.normalize_products(AmazonProducts)
        self.normalize_products(LazadaProducts)

        return

    def normalize_products(self, shop):

        products = shop.objects.all()
        cnt = 0
        for product in products:
            cnt += 1
            # if cnt <= 2896:
            #     continue
            if product.original_price == '-1' and product.current_price == '-1':
                product.delete()
            elif product.original_price == '-1':
                product.original_price = product.current_price
                product.save()
            elif product.current_price == '-1':
                product.current_price = product.original_price
                product.save()
            print ('cnt: %s ' % cnt)
        return

