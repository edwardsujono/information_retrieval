from haystack import indexes
from product.models import AmazonProducts, LazadaProducts, ShopeeProducts


class AmazonIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True)
    product_id = indexes.CharField(model_attr='product_id')
    product_name = indexes.CharField(model_attr='product_name')
    product_description = indexes.CharField(model_attr='product_description')
    product_link = indexes.CharField(model_attr='product_link')
    rating = indexes.CharField(model_attr='rating')
    image_link = indexes.CharField(model_attr='image_link')
    current_price = indexes.CharField(model_attr='current_price')
    original_price = indexes.CharField(model_attr='original_price')

    def get_model(self):
        return AmazonProducts

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class LazadaIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True)
    product_id = indexes.CharField(model_attr='product_id')
    product_name = indexes.CharField(model_attr='product_name')
    product_description = indexes.CharField(model_attr='product_description')
    product_link = indexes.CharField(model_attr='product_link')
    rating = indexes.CharField(model_attr='rating')
    image_link = indexes.CharField(model_attr='image_link')
    current_price = indexes.CharField(model_attr='current_price')
    original_price = indexes.CharField(model_attr='original_price')

    def get_model(self):
        return LazadaProducts

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ShopeeIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True)
    product_id = indexes.CharField(model_attr='product_id')
    product_name = indexes.CharField(model_attr='product_name')
    product_description = indexes.CharField(model_attr='product_description')
    product_link = indexes.CharField(model_attr='product_link')
    rating = indexes.CharField(model_attr='rating')
    image_link = indexes.CharField(model_attr='image_link')
    current_price = indexes.CharField(model_attr='current_price')
    original_price = indexes.CharField(model_attr='original_price')

    def get_model(self):
        return ShopeeProducts

    def index_queryset(self, using=None):
        return self.get_model().objects.all()