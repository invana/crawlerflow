from urllib.parse import urlparse
import uuid

def get_urn(url):
    """
    convert https://blog.scrapinghub.com/page/6/ into blog.scrapinghub.com/page/6/
    :param url:
    :return:
    """
    if "://" in url:
        return url.split("://")[1]
    return url


def get_domain(url):
    url_parsed = urlparse(url)
    return url_parsed.netloc

def generate_uuid():
    return uuid.uuid4().__str__()
