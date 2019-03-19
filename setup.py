#!/usr/bin/env python

from setuptools import setup

setup(name='invana-bot',
      version='0.0.1',
      description='A web crawler framework that can transform websites into datasets'
                  ' with Crawl, Transform and Index workflow.',
      author='Ravi Raja Merugu',
      author_email='ravi@invanalabs.ai',
      url='https://github.com/invanalabs/invana-bot',
      packages=[
          'tests',
          'invana_bot',
          'invana_bot.extractors',
          'invana_bot.fields',
          'invana_bot.httpcache',
          'invana_bot.pipelines',
          'invana_bot.spiders',
          'invana_bot.storages',
          'invana_bot.utils',
          'invana_bot.crawlers',
          'invana_bot.schedulers',
          'invana_bot.transformers',
          'invana_bot.managers'
      ],
      install_requires=[
          'Scrapy==1.6.0',
          'pymongo',
          'feedparser',
          'requests',
          'invana-transformers'
      ]
      )
