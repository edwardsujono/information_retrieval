import json
import re
from haystack.query import SearchQuerySet
import numpy as np
from nltk.corpus import stopwords
from django.conf import settings
from product.models import AmazonProducts, LazadaProducts,ShopeeProducts\
    ,AmazonComments, LazadaComments, ShopeeComments, RatingShop
from operator import itemgetter


rocchio_classifier = settings.ROCCHIO_CLASSIFER
# the result of the classifier is the primary key
vectorizer = settings.VECTORIZER_ROCCHIO
# the map between the product id and the result
map_product_id_label = settings.MAP_LABEL_WITH_Y


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


def get_recommended_items(request):

    body_unicode = request.body.decode('utf-8')
    post_data = json.loads(body_unicode)

    list_product_name = post_data.get("list_product_name")
    initial_query = post_data.get("initial_query")

    #Apply the rocchio algorithm
    #final_vector = vector_query + centroid(related_document)
    #Apply the KNN on the final vector

    initial_vector = vectorizer.transform([initial_query]).toarray()

    list_direction_vector = []

    for product_name in list_product_name:
        list_direction_vector.append(vectorizer.transform([product_name]).toarray())

    direction_vector = initial_vector + np.average(list_direction_vector, axis=0)

    # it uses the 5-NN so just 5 results is resulted
    results = rocchio_classifier.kneighbors(direction_vector, return_distance=False)

    #we do not know where the shop is so we need to query 3 databases
    #but all of them is product_id which is indexed

    list_final_product = []

    for result in results[0]:

        map_result = map_product_id_label[result]

        get_object = AmazonProducts.objects.filter(product_id=map_result)

        if len(get_object) > 0:
            list_final_product.append({"product": get_object[0], "shop": "amazon"})
            continue

        get_object = LazadaProducts.objects.filter(product_id=map_result)

        if len(get_object) > 0:
            list_final_product.append({"product": get_object[0], "shop": "lazada"})
            continue

        get_object = ShopeeProducts.objects.filter(product_id=map_result)

        if len(get_object) > 0:
            list_final_product.append({"product": get_object[0], "shop": "shopee"})
            continue

    list_json_response = []

    for result in list_final_product:

        product = result.get("product")
        shop = result.get("shop")

        list_json_response.append(
            {
                'product_name': product.product_name,
                'product_id': product.product_id,
                'product_link': product.product_link,
                'product_description': product.product_description,
                'original_price': product.original_price,
                'current_price': product.current_price,
                'image_link': product.image_link,
                'shop': shop
            }
        )

    return list_json_response


def get_return_order_with_static_score(products):

    for product in products.get('list_product'):

        if product.get('shop') == 'shopee':
            comment = ShopeeComments.objects.filter(product_id=product.get('product_link'))
            if len(comment) > 0:
                comment = comment[0]
                if comment.semantic_value:
                    product['score'] += comment.semantic_value
        elif product.get('shop') == 'amazon':
            comment = AmazonComments.objects.filter(product_id=product.get('product_link'))
            if len(comment) > 0:
                comment = comment[0]
                if comment.semantic_value:
                    product['score'] += comment.semantic_value
        else:
            comment = LazadaComments.objects.filter(product_id=product.get('product_link'))
            if len(comment) > 0:
                comment = comment[0]
                if comment.semantic_value:
                    product['score'] += comment.semantic_value

    products = sorted(products.get('list_product'), key=itemgetter('score'), reverse=True)
    return products


def get_items_semantic():

    return {
            'shopee': get_shop_all_semantic(ShopeeProducts),
            'lazada': get_shop_all_semantic(LazadaProducts),
            'amazon': get_shop_all_semantic(AmazonProducts)
        }


def get_shop_all_semantic(shop):

    all_object_comment = shop.objects.all()
    negative_comment = 0
    total_negative_comment = 0

    positive_comment = 0
    total_positive_comment = 0

    neutral_comment = 0
    total_neutral_comment = 0

    for comment in all_object_comment:
        if comment.semantic_value == -1:
            negative_comment += float(comment.rating)
            total_negative_comment += 1
        elif comment.semantic_value == 1:
            positive_comment += float(comment.rating)
            total_positive_comment += 1
        else:
            neutral_comment += float(comment.rating)
            total_neutral_comment += 1

    negative_comment = negative_comment / (total_negative_comment + 1)
    positive_comment = positive_comment / (total_positive_comment + 1)
    neutral_comment = neutral_comment / (total_neutral_comment + 1)

    total_comment = (total_neutral_comment + total_positive_comment + total_negative_comment)

    positive_radius = total_positive_comment * 1.0 / total_comment

    negative_radius = total_negative_comment * 1.0 / total_comment

    neutral_radius = total_neutral_comment * 1.0 / total_comment

    return {
        'positive': {
            'value': positive_comment,
            'total': positive_radius * 5
        },
        'negative': {
            'value': negative_comment,
            'total': negative_radius * 5
        },
        'neutral': {
            'value': neutral_comment,
            'total': neutral_radius * 5
        }
    }
