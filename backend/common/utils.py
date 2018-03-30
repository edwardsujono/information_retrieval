from django.conf import settings
import re
from nltk.corpus import stopwords

solr = settings.SOLR


def append_header_with_cors(response):

    response["Access-Control-Allow-Origin"] = '*'
    response["Access-Control-Allow-Headers"] = 'Origin, Content-Type, X-Auth-Token, Header'
    response["Access-Control-Allow-Methods"] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'

    return response


def verbose_name_to_shop_name(verbose_name):

    if "Amazon" in verbose_name:
        return "amazon"
    elif "Shopee" in verbose_name:
        return "shopee"
    else:
        return "lazada"


def product_id_to_shop_name(id):

    if "amazon" in id:
        return "amazon"
    elif "shopee" in id:
        return "shopee"
    else:
        return "lazada"


def query_more_like_this(query_string):

    result = solr.more_like_this(q=query_string, mltfl='product_name')

    return result


def preprocess_all_token(product_name):
    return removing_stopword(remove_duplicate_word_and_not_english_word(product_name.lower()))


def removing_stopword(product_name):

    word_list = product_name.split(" ")
    filtered_words = [word for word in word_list if word not in stopwords.words('english')]

    return_product_name = ""

    for word in filtered_words:
        return_product_name += word + " "

    return return_product_name[:len(return_product_name)-1]


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

