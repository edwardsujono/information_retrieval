from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from haystack.query import SearchQuerySet
from django.views.decorators.csrf import csrf_exempt
from product.models import ShopeeProducts, AmazonProducts, LazadaProducts
import json


@csrf_exempt
def search_product(request):

    if request.method == "OPTIONS":
        response = JsonResponse({"success": True})
        response["Access-Control-Allow-Origin"] = '*'
        response["Access-Control-Allow-Headers"] = 'Origin, Content-Type, X-Auth-Token'
        response["Access-Control-Allow-Methods"] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'
        return response

    body_unicode = request.body.decode('utf-8')
    post_data = json.loads(body_unicode)

    results = SearchQuerySet().all().filter(text=post_data.get("query"))
    list_json_return = {'list_product': []}

    for result in results:
        list_json_return.get('list_product').append({'product_name': result.product_name})

    response = JsonResponse(list_json_return)
    response["Access-Control-Allow-Origin"] = '*'
    response["Access-Control-Allow-Headers"] = 'Origin, Content-Type, X-Auth-Token'
    response["Access-Control-Allow-Methods"] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'
    return response


@csrf_exempt
def get_detail_item(request):

    if request.method == "OPTIONS":
        return JsonResponse({"success": True})

    get_data = request.GET

    product_id = get_data.get("product_id")
    product_type = get_data.get("shop")

    result = None

    if product_type == "shopee":
        result = ShopeeProducts.objects.get(product_id=int(product_id)).get_serialize()
    elif product_type is "amazon":
        result = AmazonProducts.objects.get(product_id=int(product_id)).get_serialize()
    elif product_type is "lazada":
        result = LazadaProducts.objects.get(product_id=int(product_id)).get_serialize()

    return JsonResponse({'success': True, 'product': result})


@csrf_exempt
def get_list_item(request):

    if request.method == "OPTIONS":
        return JsonResponse({"success": True})

    get_data = request.GET

    product_name = get_data.get("product_name")
    offset = int(get_data.get("offset"))
    limit = int(get_data.get("limit"))

    results = SearchQuerySet().all().filter(text=product_name)
    list_json_return = {'list_product': []}

    cnt = 0

    for result in results:

        if offset <= cnt < offset+limit:
            list_json_return.get('list_product').append(
                {
                    'product_name': result.product_name,
                    'product_id': result.product_id,
                    'product_link': result.product_link,
                    'product_description': result.product_description,
                    'original_price': result.original_price,
                    'current_price': result.current_price,
                    'image_link': result.image_link
                }
            )

        cnt += 1

    return JsonResponse({"list_product": list_json_return, "total": len(results)})

