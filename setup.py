#!/usr/bin/env python

from setuptools import setup

setup(name='invana-bot',
      version='0.9.14',
      description='A micro-framework to crawl the web pages with crawlers configs.'
                  ' It can use MongoDB, Elasticsearch and Solr databases to cache and save the extracted data.',
      author='Ravi Raja Merugu',
      author_email='rrmerugu@gmail.com',
      url='https://github.com/invanalabs/web-crawler-plus',
      packages=['invana_bot', 'tests',
                'invana_bot.spiders', 'invana_bot.pipelines', 'invana_bot.httpcache',
                'invana_bot.spiders.search_engines', 'invana_bot.utils'],
      install_requires=['Scrapy==1.5.0', 'pysolr==3.7.0', 'pymongo==3.6.1', 'elasticsearch-dsl==6.1.0',
                        "feedparser==5.2.1"]
      )
