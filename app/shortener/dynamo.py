import os

import boto3


def make_urls_table():
    dynamo = boto3.resource('dynamodb', region_name=(os.getenv('REGION_NAME')), endpoint_url=(os.getenv('DB_ENDPOINT')))
    return dynamo.Table(os.getenv('URLS_TABLE'))
