def append_header_with_cors(response):

    response["Access-Control-Allow-Origin"] = '*'
    response["Access-Control-Allow-Headers"] = 'Origin, Content-Type, X-Auth-Token, Header'
    response["Access-Control-Allow-Methods"] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'

    return response