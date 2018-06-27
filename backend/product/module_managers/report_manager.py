import boto3
import requests
from io import BytesIO


def generate_report(list_item, keyword, limit):

    client = boto3.client('rekognition')

    number_success = 0
    success = False
    number_fail = 0
    number_error = 0
    counter = 0
    list_fail_item = []

    for item in list_item:

        response = requests.get(item.image_link)
        img = BytesIO(response.content)

        try:
            response = client.detect_labels(Image={'Bytes': img.getvalue()})
        except Exception:
            number_error += 1
            continue

        for label in response.get('Labels'):
            if keyword.lower() == label.get('Name').lower():
                number_success += 1
                success = True

        if not success:
            number_fail += 1
            list_fail_item.append(
                {
                    'product_name': item.product_name,
                    'product_solr_id': item.id,
                    'product_id': item.product_id,
                    'product_link': item.product_link,
                    'product_description': item.product_description,
                    'original_price': item.original_price,
                    'current_price': item.current_price,
                    'image_link': item.image_link,
                    'shop': "General",
                    'score': item.score
                }
            )

        success = False

        counter += 1

        if counter == limit:
            break

    return {'num_fails': number_fail,
            'num_success': number_success,
            'list_fail_item': list_fail_item}
