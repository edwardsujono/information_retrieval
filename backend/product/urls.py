from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^search_product/(?P<product_name>\w{0,50})$', views.search_product, name='search_product'),
]