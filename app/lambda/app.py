from shortener.redirect import redirect
from shortener.dynamo import make_urls_table

urls_table = make_urls_table()


def redirect_handler(event, context):
    return redirect(urls_table, event)
