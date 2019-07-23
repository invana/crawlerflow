def default_extractor_fn(response=None):
    """

    """
    url = response.url

    data = {}
    if "/contact" in url:
        data["page_type"] = "contact"
    elif "/blog/" in url:
        data["page_type"] = "blog"
    elif "/about" in url:
        data["page_type"] = "about"
    elif "/service" in url:
        data["page_type"] = "service"
    elif "/product" in url:
        data["page_type"] = "product"
    elif url.strip("/").count("/") == 2:  # this can be improved.
        data["page_type"] = "homepage"
    else:
        data["page_type"] = "others"
    return data
