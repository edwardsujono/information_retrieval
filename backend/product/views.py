from django.http import JsonResponse
from haystack.query import SearchQuerySet
from django.views.decorators.csrf import csrf_exempt
from product.models import ShopeeProducts, AmazonProducts, LazadaProducts
from common.utils import append_header_with_cors, verbose_name_to_shop_name
from . import search_manager


@csrf_exempt
def search_product(request):

    if request.method == "OPTIONS":
        return append_header_with_cors(JsonResponse({"success": True}))

    return append_header_with_cors(JsonResponse(search_manager.get_suggestion_word(request)))


@csrf_exempt
def get_detail_item(request):

    if request.method == "OPTIONS":
        return append_header_with_cors(JsonResponse({"success": True}))

    get_data = request.GET

    product_id = get_data.get("product_id")
    product_type = get_data.get("shop")

    result = None

    if product_type == "shopee":
        result = ShopeeProducts.objects.get(product_id=int(product_id)).get_serialize()
    elif product_type == "amazon":
        result = AmazonProducts.objects.get(product_id=int(product_id)).get_serialize()
    elif product_type == "lazada":
        result = LazadaProducts.objects.get(product_id=int(product_id)).get_serialize()

    return append_header_with_cors(JsonResponse({'success': True, 'product': result}))


@csrf_exempt
def get_list_item(request):

    if request.method == "OPTIONS":
        return append_header_with_cors(JsonResponse({"success": True}))

    get_data = request.GET

    product_name = get_data.get("product_name")
    offset = int(get_data.get("offset"))
    limit = int(get_data.get("limit"))
    shops = get_data.get("shop")

    results = SearchQuerySet().all().filter(product_name=product_name)
    list_json_return = {'list_product': []}

    cnt = 0

    if shops is not None:

        list_shop = shops.split(",")

        results = list(
            filter(lambda result: verbose_name_to_shop_name(result.verbose_name) in list_shop, results)
        )

    for result in results:

        verbose_shop = verbose_name_to_shop_name(result.verbose_name)

        if offset <= cnt < offset+limit:
            list_json_return.get('list_product').append(
                {
                    'product_name': result.product_name,
                    'product_solr_id': result.id,
                    'product_id': result.product_id,
                    'product_link': result.product_link,
                    'product_description': result.product_description,
                    'original_price': result.original_price,
                    'current_price': result.current_price,
                    'image_link': result.image_link,
                    'shop': verbose_shop,
                    'score': result.score
                }
            )

        cnt += 1

    return append_header_with_cors(
        JsonResponse({"list_product": search_manager.get_return_order_with_static_score(
                list_json_return), "total": len(results)}))


@csrf_exempt
def get_recommended_item(request):

    if request.method == "OPTIONS":
        return append_header_with_cors(JsonResponse({"success": True}))

    return append_header_with_cors(
        JsonResponse({"list_product": search_manager.get_recommended_items(request)})
    )


@csrf_exempt
def get_items_semantic(request):

    if request.method == "OPTIONS":
        return append_header_with_cors(JsonResponse({"success": True}))

    return append_header_with_cors(
        JsonResponse(search_manager.get_items_semantic())
    )
