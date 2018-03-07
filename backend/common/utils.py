def append_header_with_cors(response):

    response["Access-Control-Allow-Origin"] = '*'
    response["Access-Control-Allow-Headers"] = 'Origin, Content-Type, X-Auth-Token, Header'
    response["Access-Control-Allow-Methods"] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'

    return response


def verbose_name_to_shop_name(verbose_name):

    if "Amazon" in verbose_name:
        return "Amazon"
    elif "Shopee" in verbose_name:
        return "Shopee"
    else:
        return "Lazada"
