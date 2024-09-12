from urllib.parse import urlparse
from validators.url import url
from validators.length import length


def get_normalize_name(name):
    url_parse = urlparse(name)
    return ''.join([url_parse.scheme, '://', url_parse.hostname])


def is_valid(name):
    return url(name) and length(name, max_val=255)
