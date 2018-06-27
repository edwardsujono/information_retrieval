from django.conf.urls import include, url
from . import views
from product.module_views import report_views

urlpatterns = [
    url(r'^search_product/$', views.search_product, name='search_product'),
    url(r'^get_detail_item/$', views.get_detail_item, name='get_detail_item'),
    url(r'^get_list_item/$', views.get_list_item, name='get_list_item'),
    url(r'^get_list_optimized_item/$', views.get_list_item_optimized, name='get_list_optimized_item'),
    url(r'^get_recommended_items/$', views.get_recommended_item, name='get_list_recommended_item'),
    url(r'^get_items_semantic/$', views.get_items_semantic, name='get_items_semantic'),
    url(r'^generate_report/', report_views.generate_report, name='generate_report')
]