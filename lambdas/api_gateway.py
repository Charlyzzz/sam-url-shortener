import json


def html_response(body):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": 'text/html'
        },
        "body": body
    }


def json_response(status_code, body=None):
    if body is None:
        body = {}
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def error(e):
    return json_response(500, {"error": e})


def redirect(url):
    return {
        "statusCode": 301,
        "headers": {
            "Location": url
        }
    }


def not_found(resource_id):
    return json_response(404, {"error": f'slug {resource_id} was not found'})
