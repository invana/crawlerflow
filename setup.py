#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='web-scraper',
    version='0.0.0',
    description='scrape data from web with no code (just YAML configs)',
    author='Ravi Raja Merugu',
    author_email='ravi@invana.io',
    url='https://github.com/invana/web-scraper',
    packages=find_packages(
        where="src",
        exclude=("dist", "docs", "examples", "tests", "examples-configs")
    ),
    install_requires=[
        'Scrapy==2.11.0',
        'PyYAML==6.0.1',
        'pymongo==4.5.0',
        'python-slugify==8.0.1' 
    ]
)