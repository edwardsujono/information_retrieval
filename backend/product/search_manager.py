import json
import re
from haystack.query import SearchQuerySet
from nltk.corpus import stopwords


def get_suggestion_word(request):

    body_unicode = request.body.decode('utf-8')
    post_data = json.loads(body_unicode)

    query_data = post_data.get("query")
    list_json_return = {'list_product': []}

    if len(query_data.split(" ")) == 0:
        return list_json_return

    check_start_query_word = query_data.split(" ")[0]
    treshold_word_count = len(query_data.split(" "))

    results = SearchQuerySet().all().filter(product_name=query_data)

    dict_filter_token = {}

    limit = 100

    # calculating the token number
    if len(results) > limit:
        results = results[:limit]

    for result in results:

        list_word = result.product_name.split(" ")
        list_word = [word for word in list_word if word not in stopwords.words('english')]

        for word in list_word:
            if dict_filter_token.get(word.lower()) is None:
                dict_filter_token[word.lower()] = 0

            dict_filter_token[word.lower()] += 1


    set_allowed_token = set()

    for key, value in dict_filter_token.items():

        if value > 3:
            set_allowed_token.add(key)

    set_word = set()

    for result in results:

        list_word = result.product_name.split(" ")
        list_word = [word for word in list_word if word not in stopwords.words('english')]
        word_filter = ""

        start_used = False

        for word in list_word:

            if word.lower() == check_start_query_word.lower():
                start_used = True

            if word.lower() in set_allowed_token and start_used:
                word_filter += word.lower() + " "

        # stripping space
        word_filter = remove_duplicate_word_and_not_english_word(word_filter.strip(" "))

        # just allowed the return string length to be more than the query
        if len(word_filter.split(" ")) > treshold_word_count and word_filter not in set_word:

            set_word.add(word_filter)
            list_json_return.get('list_product').append(
                {'product_name': word_filter}
            )

    return list_json_return


def remove_duplicate_word_and_not_english_word(word):

    word_return = ""

    word = re.sub(r'([^\s\w]|_)+', '', word)
    list_token = word.split(" ")
    check_set = set()

    for token in list_token:

        if token not in check_set and (token.isalpha() or token.isnumeric()):
            check_set.add(token)
            word_return += token + " "

    word_return = word_return.strip(" ")

    return word_return
