# Invana Bot

A web crawler framework that can transform websites into datasets using Crawl, 
Transform and Index strategy. The best part is you don't need to code, you just need 
 to define the extraction and traversal configurations in yaml. 


InvanaBot uses [MongoDB](https://www.mongodb.com/) as default database for caching and storage.



**NOTE: This project is under active development**

[![Build Status](https://travis-ci.org/invanalabs/invana-bot.svg?branch=master)](https://travis-ci.org/invanalabs/invana-bot) 
[![codecov](https://codecov.io/gh/invanalabs/invana-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/invanalabs/invana-bot) 


[**Features**](#features) | [**Install**](#install) | [**Usage**](#usage) | [**Documentation**](#documentation) | [**Support**](#support)


## Features

1. crawlers in the form of json configuration.

2. Define traversals from one parser to another.

3. Use standard extractors to scrape data like Tables, Paragraphs, Meta data of the page.

4. Define custom extractors to scrapy the data in the format you want in yaml config.

5. MongoDB as default Cache and Storage Database.

7. Transform and Index - You can add your data transformation logic, that can format 
the crawled data into another format and index into use specified storage. 



## Install

```bash
pip install git+https://github.com/invanalabs/invana-bot#egg=invana_bot
# This project is under constant development and might brake any previous implementation.
```



## Usage

To run a single website crawler, to extract information from one website only.

```bash
python3 bin/bot.py --path ./examples/run-single-crawler/ --type=single
```

To run a complex crawling strategy where crawling and data extraction happenings through multiple 
websites with traversal definitions.


```bash
python3 bin/bot.py --path ./examples/cti-flow-runner/ --type=cti
```


## Documentation

Refer examples in the `examples/` folder or check [doc/index.md](docs/index.md) for more details.


## Support

Few features like IP rotation, headless browsing, data backups, scheduling and monitoring are 
available in our [InvanaBot Cloud](https://invanalabs.ai/invana-bot.html) version.

For any futher queries or dedicated support, please feel free to [contact us](http://invanalabs.ai/contact-us.html)