from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^search_product/$', views.search_product, name='search_product'),
    url(r'^get_detail_item/$', views.get_detail_item, name='get_detail_item'),
    url(r'^get_list_item/$', views.get_list_item, name='get_list_item'),
]