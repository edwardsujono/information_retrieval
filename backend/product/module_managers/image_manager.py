import boto3
import requests
from io import BytesIO


def update_score_with_image(list_item, keyword):

    normalize_score_of_item(list_item)

    client = boto3.client('rekognition')

    for item in list_item.get('list_product'):

        response = requests.get(item.get('image_link'))
        img = BytesIO(response.content)

        try:
            response = client.detect_labels(Image={'Bytes': img.getvalue()})
        except Exception:
            return

        for label in response.get('Labels'):

            item['score'] = item['score'] * 0.5

            if keyword.lower() == label.get('Name').lower():
                item['score'] = 0.5 + item['score']
                break


def normalize_score_of_item(list_item):

    min_score = 1000
    max_score = -1

    for item in list_item.get('list_product'):

        if item.get('score') > max_score:
            max_score = item.get('score')

        if item.get('score') < min_score:
            min_score = item.get('score')

    for item in list_item.get('list_product'):
        item['score'] = (item['score'] - min_score) * 1.0 / (max_score - min_score)
