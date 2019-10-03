import decimal
import json
import boto3
import os

from botocore.exceptions import ClientError

URLS = os.getenv('URLS_TABLE')
urls_table = boto3.resource('dynamodb').Table(URLS)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):
    print(event)
    slug = event['pathParameters']['slug']
    if slug is None:
        return response(400, {"error": 'slug is missing'})
    try:
        get_item_response = urls_table.get_item(
            Key={
                'id': slug
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return response(500, {"error": e})
    else:
        if 'Item' in get_item_response:
            item = get_item_response['Item']
            url = item['url']
            return redirect(url)
        else:
            return not_found(slug)


def response(status_code, body=None):
    if body is None:
        body = {}
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
    }


def error(e):
    return response(500, {"error": e})


def redirect(url):
    return {
        "statusCode": 301,
        "headers": {
            "Location": url
        }
    }


def not_found(resource_id):
    return response(404, {"error": f'slug {resource_id} was not found'})
