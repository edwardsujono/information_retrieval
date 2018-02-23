from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import pysolr

# Create your views here.


def search_product(request, product_name):
    return JsonResponse({'success': product_name})
