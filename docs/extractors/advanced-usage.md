# Advanced Usage


Here is the documentation on advanced level usage.

## Selector Explained



## Running Extractor manually


```python

from invana_bot.extractors import ParagraphsExtractor

# response should of data type : scrapy.http.response.html.HtmlResponse

response = <self.response of the Spider>
extracted_data = ParagraphsExtractor(response=response, extractor=None, parser_id="paragraphs").run()

```

