#!/usr/bin/env python

from setuptools import setup

setup(name='invana-bot',
      version='0.0.8',
      description='A web crawler framework that can transform websites into datasets'
                  ' with Crawl, Transform and Index workflow.',
      author='Ravi Raja Merugu',
      author_email='ravi@invanalabs.ai',
      url='https://github.com/invanalabs/invana-bot',
      packages=[
          'invana_bot',
          'invana_bot.extractors',
          'invana_bot.fields',
          'invana_bot.httpcache',
          'invana_bot.jobs',
          'invana_bot.managers',
          'invana_bot.storages',
          'invana_bot.runners',
          'invana_bot.spiders',
          'invana_bot.storages',
          'invana_bot.transformers',
          'invana_bot.utils'
      ],
      install_requires=[
          'Scrapy==1.6.0',
          'pymongo',
          'feedparser',
          'requests',
          'invana-transformers'
      ]
      )
