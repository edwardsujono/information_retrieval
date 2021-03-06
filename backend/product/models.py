from django.db import models
from haystack import indexes

# Create your models here.


class RatingShop(models.Model):

    shop = models.CharField(max_length=1000)
    rating = models.FloatField()

    class Meta:
        db_table = 'rating_shop'


class AmazonProducts(models.Model):

    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=1000)
    original_price = models.CharField(max_length=20)
    current_price = models.CharField(max_length=20)
    product_description = models.CharField(max_length=5000)
    product_link = models.CharField(max_length=1000)
    rating = models.CharField(max_length=10)
    image_link = models.CharField(max_length=1000)
    semantic_value = models.IntegerField()

    class Meta:
        db_table = 'amazon_products'

    def get_serialize(self):

        return {
            "id": self.product_id,
            "product_name": self.product_name,
            "original_price": self.original_price,
            "current_price": self.current_price,
            "product_description": self.product_description,
            "product_link": self.product_link,
            "rating": self.rating,
            "image_link": self.image_link,
            "semantic_value": self.semantic_value
        }


class AmazonComments(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=1000)
    comment = models.CharField(max_length=1000)
    semantic_value = models.IntegerField()

    class Meta:
        db_table = 'amazon_comments'

    def get_serialize(self):

        return {
            "product_id": self.product_id,
            "comment": self.comment
        }


class ShopeeProducts(models.Model):

    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=1000)
    original_price = models.CharField(max_length=20)
    current_price = models.CharField(max_length=20)
    product_description = models.CharField(max_length=5000)
    product_link = models.CharField(max_length=1000)
    rating = models.CharField(max_length=10)
    image_link = models.CharField(max_length=1000)
    semantic_value = models.IntegerField()

    class Meta:
        db_table = 'shopee_products'

    def get_serialize(self):

        return {
            "id": self.product_id,
            "product_name": self.product_name,
            "original_price": self.original_price,
            "current_price": self.current_price,
            "product_description": self.product_description,
            "product_link": self.product_link,
            "rating": self.rating,
            "image_link": self.image_link,
            "semantic_value": self.semantic_value
        }


class ShopeeComments(models.Model):
    
    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=1000)
    comment = models.CharField(max_length=1000)
    semantic_value = models.IntegerField()

    class Meta:
        db_table = 'shopee_comments'

    def get_serialize(self):

        return {
            "product_id": self.product_id,
            "comment": self.comment
        }


class LazadaProducts(models.Model):

    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=1000)
    original_price = models.CharField(max_length=20)
    current_price = models.CharField(max_length=20)
    product_description = models.CharField(max_length=5000)
    product_link = models.CharField(max_length=1000)
    rating = models.CharField(max_length=10)
    image_link = models.CharField(max_length=1000)
    semantic_value = models.IntegerField()

    class Meta:
        db_table = 'lazada_products'

    def get_serialize(self):
        return {
            "id": self.product_id,
            "product_name": self.product_name,
            "original_price": self.original_price,
            "current_price": self.current_price,
            "product_description": self.product_description,
            "product_link": self.product_link,
            "rating": self.rating,
            "image_link": self.image_link,
            "semantic_value": self.semantic_value
        }


class LazadaComments(models.Model):
    
    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=1000)
    comment = models.CharField(max_length=1000)
    semantic_value = models.IntegerField()

    class Meta:
        db_table = 'lazada_comments'

    def get_serialize(self):

        return {
            "product_id": self.product_id,
            "comment": self.comment
        }


# Product Name to store all the name of the product that has been pre-processed

class ProductName(models.Model):

    product_id = models.AutoField(primary_key=True)
    product_link = models.CharField(max_length=1000)
    product_name = models.CharField(max_length=1000)

    class Meta:
        db_table = 'product_names'


# Product token with the number of token existed

class ProductTokenCount(models.Model):

    token_id = models.AutoField(primary_key=True)
    token_name = models.CharField(max_length=100)
    token_count = models.IntegerField()

    class Meta:
        db_table = 'product_token_counts'
