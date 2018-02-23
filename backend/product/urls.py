from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^search_product/$', views.search_product, name='search_product'),
]