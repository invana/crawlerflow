from webcrawler.utils import example_config
from webcrawler.parser import crawler

settings = {
    'FEED_URI': 'result.json'
}

if __name__ == '__main__':
    crawler(config=example_config, settings=settings)
