#!/usr/bin/env python

from setuptools import setup

setup(name='invana-bot',
      version='0.0.0a',
      description='A batteries included crawler framework built on top of scrapy for scale and intelligent crawling.',
      author='Ravi Raja Merugu',
      author_email='rrmerugu@gmail.com',
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
      ],
      install_requires=['Scrapy==1.6.0',
                        'pymongo',
                        "feedparser==5.2.1"
                        ]
      )
