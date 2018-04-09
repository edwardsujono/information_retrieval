from django.core.management.base import BaseCommand
from product.models import ShopeeProducts, LazadaProducts,\
    AmazonProducts, LazadaComments, ShopeeComments, AmazonComments


class Command(BaseCommand):

    def handle(self, *args, **options):

        # this will build the indexer for the auto complete
        # self.update_in_semantic_value(ShopeeComments, ShopeeProducts)
        # self.update_in_semantic_value(LazadaComments, LazadaProducts)
        self.update_in_semantic_value(AmazonComments, AmazonProducts)
        return

    def update_in_semantic_value(self, shop, products):

        all_object_comment = shop.objects.all()
        cnt = 0

        for comment in all_object_comment:
            product = products.objects.filter(product_link__istartswith=comment.product_id)
            # print('product id: %s ' % comment.product_id)

            if len(product) > 0:
                product = product[0]
                print('product semantic_value: %s ' % product.semantic_value)
                if comment.semantic_value:
                    product.semantic_value = comment.semantic_value
                    product.save()
                    print(cnt)
                    cnt += 1
