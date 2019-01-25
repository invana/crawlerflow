#!/usr/bin/env python

from setuptools import setup

setup(name='invana-bot',
      version='dev',
      description='A batteries included crawler framework built on top of scrapy for scale and intelligent crawling.',
      author='Ravi Raja Merugu',
      author_email='rrmerugu@gmail.com',
      url='https://github.com/invanalabs/invana-bot',
      packages=[
          'tests',
          'invana_bot',
          'invana_bot.analysers',
          'invana_bot.httpcache',
          'invana_bot.pipelines',
          'invana_bot.spiders',
          'invana_bot.utils',
      ],
      install_requires=['Scrapy==1.5.0', 'pysolr==3.7.0', 'pymongo==3.6.1', 'elasticsearch-dsl==6.1.0',
                        "feedparser==5.2.1"]
      )
