# Invana Bot

A web crawler framework that can transform websites into datasets with Crawl, 
Transform and Index workflow. InvanaBot uses [MongoDB](https://www.mongodb.com/)
 as default database for caching and storage.


**NOTE: This project is under active development**

[![Build Status](https://travis-ci.org/invanalabs/invana-bot.svg?branch=master)](https://travis-ci.org/invanalabs/invana-bot) 
[![codecov](https://codecov.io/gh/invanalabs/invana-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/invanalabs/invana-bot) 


[**Features**](#features) | [**Install**](#install) | [**Usage**](#usage) | [**Support**](#support) | [**Documentation**](#documentation)


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
## cti_flow/cti_manifest.json 
{
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
## cti_flow/cti_transformations.py

def transformation_fn(results):
    """
    write your data transformation logic
    """
    results_cleaned = results
    return results_cleaned

```

```bash

python3 bin/bot.py --path ./cti_flow

```

## Documentation

Refer examples in the `examples/` folder or check [doc/index.md](docs/index.md) for more details.


## Support

Few features like IP rotation, headless browsing, data backups, scheduling and monitoring are 
available in our [InvanaBot Cloud](https://invanalabs.ai/invana-bot.html) version.

For any futher queries or dedicated support, please feel free to [contact us](http://invanalabs.ai/contact-us.html)