#!/usr/bin/env python

from setuptools import setup, find_packages, __version__ as setuptools_version

requirements = open('./requirements.txt', 'r').readlines()

setup(name='invana-bot',
      version='0.1.1',
      description='A web crawler framework that can transform websites into datasets'
                  ' with Crawl, Transform and Index workflow.',
      author='Ravi Raja Merugu',
      author_email='ravi@invanalabs.ai',
      url='https://github.com/invanalabs/invana-bot',
      packages=find_packages(
          exclude=("bin", "dist", "docs", "example", "tests",)
      ),
      install_requires=[requirement for requirement in requirements],
      entry_points={
          'console_scripts': ['invana-bot = invana_bot.cmd.run:invana_bot_run']
      },
      )
