# Invana Bot

A web crawler framework that can transform websites into datasets with Crawl, 
Transform and Index workflow. InvanaBot uses [MongoDB](https://www.mongodb.com/)
 as default database for caching and storage.


**NOTE: This project is under active development**

[![Build Status](https://travis-ci.org/invanalabs/invana-bot.svg?branch=master)](https://travis-ci.org/invanalabs/invana-bot) 
[![codecov](https://codecov.io/gh/invanalabs/invana-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/invanalabs/invana-bot) 


[**Features**](#features) | [**Install**](#install) | [**Usage**](#usage) | [**Support**](#support) | [**Documentation**](/docs/index.md)


## Features

1. crawlers in the form of json configuration.

2. Define traversals from one parser to another.

3. Use standard extractors to scrape data like Tables, Paragraphs, Meta data of the page.

4. Define custom extractors to scrapy the data in the format you want -
 list of objects, list of strings, or dictionaries.

5. MongoDB as default Cache and Storage Database.

7. Transform and Index - You can add your data transformation logic, that can format 
the crawled data into another format and index into use specified storage. 



## Install

```bash
pip install git+https://github.com/invanalabs/invana-bot#egg=invana_bot
# This project is under constant development and might brake any previous implementation.
```



## Usage

```python
## cti_manifest.json
cti_manifest = {
  "cti_id": "example_cti_flow",
  "init_crawler": {...},
  "crawlers": [...],
  "transformations": [...],
  "indexes": [...],
  "callbacks": [...],
  "context": {
    "author": "https://github.com/rrmerugu",
    "description": "Crawler that scrapes invanalabs xyz"
  }
}
```

```python

from invana_bot.crawlers.generic import InvanaBotWebCrawler
from invana_bot.settings import DEFAULT_SETTINGS
from invana_bot.managers.manifest import ETIManifestManager
import eti_transformations

if __name__ == '__main__':
    manifest_manager = ETIManifestManager(cti_config_path="./", eti_transformations_module=eti_transformations)
    cti_manifest = manifest_manager.get_manifest()
    crawler = InvanaBotWebCrawler(
        settings=DEFAULT_SETTINGS
    )
    context = cti_manifest.get("context")
    job = crawler.create_job(
        cti_manifest=cti_manifest,
        context=context
    )
    print("job", job)
    crawler.start_job(job=job)


```


## Support

Feel free to [contact us](http://invanalabs.ai/contact-us/) for any further support. Few features like 
IP rotation, headless browsing, data backups, scheduling and monitoring are 
available in our [InvanaBot Cloud](http://invanalabs.ai/product/invana-bot) version.