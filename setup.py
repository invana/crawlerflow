#!/usr/bin/env python

from setuptools import setup, find_packages, __version__ as setuptools_version


setup(name='invana-bot',
      version='0.1.35',
      description='A web spider framework that can transform websites into datasets'
                  ' with Crawl, Transform and Index workflow.',
      author='Ravi Raja Merugu',
      author_email='ravi@invanalabs.ai',
      url='https://github.com/invanalabs/invana-bot',
      packages=find_packages(
          exclude=("bin", "dist", "docs", "example", "tests", "dist")
      ),
      install_requires=[
          'elasticsearch==6.1.1',
          'feedparser==5.2.1',
          'lxml==4.1.1',
          'pymongo==3.7.2',
          'requests==2.21.0',
          'Scrapy==1.6.0',
          'pyyaml==5.1',
          'python-slugify '
      ],
      entry_points={
          'console_scripts': ['invana-bot = invana_bot.cmd.run:invana_bot_run']
      },
      )
