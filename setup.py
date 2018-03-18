#!/usr/bin/env python

from setuptools import setup

setup(name='web-crawler-plus',
      version='0.9.10',
      description='A micro-framework to crawl the web pages with crawlers configs.'
                  ' It can use MongoDB, Elasticsearch and Solr databases to cache and save the extracted data.',
      author='Ravi Raja Merugu',
      author_email='rrmerugu@gmail.com',
      url='https://github.com/invanatech/web-crawler-plus',
      packages=['webcrawler', 'tests',
                'webcrawler.spiders', 'webcrawler.pipelines', 'webcrawler.httpcache',
                'webcrawler.spiders.search_engines', 'webcrawler.utils'],
      install_requires=['Scrapy==1.5.0', 'pysolr==3.7.0', 'pymongo==3.6.1', 'elasticsearch-dsl==6.1.0',
                        "feedparser==5.2.1"]
      )
