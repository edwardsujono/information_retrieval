from django.core.management.base import BaseCommand
from product.models import AmazonComments, LazadaComments, ShopeeComments
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **options):

        # this will build the indexer for the auto complete
        # self.update_db_from_csv('amazon_comments_sentiment.csv')
        # self.update_db_from_csv('lazada_comments_sentiment.csv')
        self.update_db_from_csv('shopee_comments_sentiment.csv')
        return

    def update_db_from_csv(self, file_name):

        obj_update = pd.read_csv(file_name)
        cnt = 0

        for id, sentiment in zip(obj_update['id'], obj_update['sentiment']):
            if 'amazon' in file_name:
                update = AmazonComments.objects.filter(product_id=id)
            elif 'lazada' in file_name:
                update = LazadaComments.objects.filter(product_id=id)
            else:
                update = ShopeeComments.objects.filter(product_id=id)

            if len(update) == 0:
                continue

            update = update[0]
            update.semantic_value = sentiment
            update.save()
            print (cnt)
            cnt += 1