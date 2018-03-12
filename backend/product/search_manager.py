import json
from haystack.query import SearchQuerySet


def get_suggestion_word(request):

    body_unicode = request.body.decode('utf-8')
    post_data = json.loads(body_unicode)

    results = SearchQuerySet().all().filter(text=post_data.get("query"))
    list_json_return = {'list_product': []}

    dict_filter_token = {}

    for result in results:

        list_word = result.split(" ")

        for word in list_word:
            if dict_filter_token.get(word.lower()):
                dict_filter_token[word.lower] = 0

            dict_filter_token[word.lower] += 1

    set_allowed_token = set()

    for key, value in dict_filter_token.items():

        if value > 1:
            set_allowed_token.add(key)

    for result in results:

        list_word = result.split(" ")
        word_filter = ""

        for word in list_word:

            if word in set_allowed_token:
                word_filter += word + " "

        list_json_return.get('list_product').append(
            {'product_name': word_filter[:len(word_filter)-1]}
        )

    return list_json_return
