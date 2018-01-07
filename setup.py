#!/usr/bin/env python

from distutils.core import setup

setup(name='web-crawler',
      version='0.999',
      description='A micro-framework to crawl the web pages - blogs/rss using defined configurations',
      author='Ravi RT Merugu',
      author_email='rrmerugu@gmail.com',
      url='https://github.com/invaana/web-crawler',
      packages=['webcrawler', ],
      install_requires=['scrapy']
      )
