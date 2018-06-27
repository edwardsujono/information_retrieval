# default library
from django.views.decorators.csrf import csrf_exempt

# your library
from product.module_managers import report_manager

# common library
from common.utils import append_header_with_cors
from django.http import JsonResponse
from haystack.query import SearchQuerySet


@csrf_exempt
def generate_report(request):

    if request.method == "OPTIONS":
        return append_header_with_cors(JsonResponse({"success": True}))

    get_data = request.GET

    keyword = get_data.get("keyword")
    limit = int(get_data.get("limit"))

    results = SearchQuerySet().all().filter(product_name=keyword)

    return append_header_with_cors(
        JsonResponse(report_manager.generate_report(list_item=results, keyword=keyword, limit=limit))
    )
