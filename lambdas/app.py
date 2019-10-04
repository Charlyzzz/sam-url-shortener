from .redirect import redirect
from .dynamo import make_urls_table

urls_table = make_urls_table()


def redirect_lambda_handler(event, context):
    redirect(urls_table, event)
