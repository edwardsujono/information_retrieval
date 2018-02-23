from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import pysolr

# Create your views here.


def search_product(request):

    list_mock_return = {'list_product': []}

    for i in range(10):
        list_mock_return.get('list_product').append({"product_name": "test_%s" % i})

    return JsonResponse(list_mock_return)
