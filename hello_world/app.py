import decimal
import json
import boto3
import os

from botocore.exceptions import ClientError

URLS = os.getenv('URLS_TABLE')
DYNAMO_ENDPOINT_URL = os.getenv('DB_ENDPOINT')
REGION_NAME = os.getenv('REGION_NAME')
urls_table = boto3.resource('dynamodb', region_name=REGION_NAME, endpoint_url=DYNAMO_ENDPOINT_URL).Table(URLS)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):
    user_agent = event['headers']['User-Agent'].lower()
    slug = event['pathParameters']['slug']
    if slug is None:
        return response(400, {"error": 'slug is missing'})
    if any(word in user_agent for word in ["bot", "facebookexternalhit"]):
        print("detected scrapping")
        return bot_landing()
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


def bot_landing():
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": 'text/html'
        },
        "body": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta property="og:title" content="The Rock" />
    <meta property="og:type" content="video.movie" />
    <meta property="og:url" content="http://www.imdb.com/title/tt0117500/" />
    <meta property="og:image" content="http://ia.media-imdb.com/images/rock.jpg" />
</head>
<body>
</body>
</html>
"""
    }


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
