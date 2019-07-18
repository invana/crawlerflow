# Pythonic Extractor


This extractor is unique from the rest of the extractors, because it gives more power
to the directly to the user, giving full access to html content.

The extractor is available at `invana_bot.extractors.PythonBasedExtractor`. 


User has to write a python function in `ib_functions.py` and the name of the function 
should be specified in the `manifest.yml` as shown in the example.



```yaml
# in manifest.yml
- spider_id: default_spider
  allowed_domains:
    - "github.com"
  extractors:
  - extractor_id: page_detection
    extractor_type: PythonBasedExtractor
    extractor_fn: default_extractor_fn
```

```python
# ib_functions.py

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

```