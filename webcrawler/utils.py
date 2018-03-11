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
    if "://" in url:
        url = url.split("://")[1]
    if "/" in url:
        url = url.split("/")[0]
    return url.strip()
