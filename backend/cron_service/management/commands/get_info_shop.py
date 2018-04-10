from django.core.management.base import BaseCommand
from product.models import ShopeeProducts, LazadaProducts,\
    AmazonProducts


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = {
            'shopee': self.get_info_shop(ShopeeProducts),
            'lazada': self.get_info_shop(LazadaProducts),
            'amazon': self.get_info_shop(AmazonProducts)
        }
        print ('data: %s' % data)

    def get_info_shop(self, Shop):
        products = Shop.objects.all()

        total_word = 0
        set_token = set()

        for product in products:

            list_word = product.product_name.strip(" ").split(" ")

            for word in list_word:
                total_word += 1
                set_token.add(word.lower())

        return {
            'total_word': total_word,
            'unique_token': len(set_token)
        }
