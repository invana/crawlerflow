import pytest
import os

from web_scraper.extractors import CustomContentExtractor
import yaml

html_text = """
<html>
    <body>
        <h1>Hello, Parsel!</h1>
        <ul class="header">
            <li><a href="http://example.com">Link 1</a></li>
            <li><a href="http://scrapy.org">Link 2</a></li>
        </ul>
        <img class="banner-pic" src="https://placehold.co/600x400.png">
        <main>Main text here</main>
    </body>
</html>
"""
extractor_config ="""
---
title:
  selector: h1::text
cover_pic:
  selector: .banner-pic::attr(src)
header_links:
  selector: .header li a
  type:
    - DictField
  fields:
    link:
      selector: ::attr(href)
    text:
      selector: ::text
post_content_html:
  selector: main
"""

@pytest.fixture(scope="function")
def html_extractor() -> str:
    extractor_config_json = yaml.safe_load(extractor_config)
    return CustomContentExtractor(html_text, extractor_config_json)