import datetime


def set_cache_headers(response):
    max_age = (3600 * 24) * 7
    response['Cache-Control'] = f'max-age={max_age}'  # Cache for one hour

    response['Expires'] = datetime.datetime.now() + datetime.timedelta(days=4)

    return response
