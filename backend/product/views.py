from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from haystack.query import SearchQuerySet
from django.views.decorators.csrf import csrf_exempt
from product.models import ShopeeProducts
import json


@csrf_exempt
def search_product(request):

    body_unicode = request.body.decode('utf-8')
    post_data = json.loads(body_unicode)

    results = SearchQuerySet().all().filter(text=post_data.get("query"))
    list_json_return = {'list_product': []}

    for result in results:
        list_json_return.get('list_product').append({'product_name': result.product_name})

    return JsonResponse(list_json_return)
