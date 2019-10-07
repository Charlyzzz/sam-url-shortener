from botocore.exceptions import ClientError

from .api_gateway import json_response, html_response, not_found
from .api_gateway import redirect as gateway_redirect


def redirect(urls_table, event):
    user_agent = event['headers']['User-Agent'].lower()
    slug = event['pathParameters']['slug']
    if slug is None:
        return json_response(400, {"error": 'slug is missing'})
    if any(word in user_agent for word in ["bot", "facebookexternalhit"]):
        print("detected scrapping")
        return html_response(bot_landing)
    try:
        found_url_entry = urls_table.get_item(Key={'id': slug})
    except ClientError as e:
        print(e.response['Error']['Message'])
        return json_response(500, {"error": e})
    else:
        if 'Item' in found_url_entry:
            item = found_url_entry['Item']
            url = item['url']
            return gateway_redirect(url)
        else:
            return not_found(slug)


bot_landing = """
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
