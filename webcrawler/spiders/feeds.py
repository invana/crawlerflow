from scrapy.spiders import XMLFeedSpider
from webcrawler.utils.url import get_domain


class GenericFeedSpider(XMLFeedSpider):
    name = "generic_feed_spider"
    itertag = 'item'
    iterator = 'xml'  # This is actually unnecessary, since it's the default value

    def get_or_none(self, selector):
        try:
            return selector.extract_first()
        except Exception as e:
            print(e)
            return None

    def parse_node(self, response, node):
        title = self.get_or_none(node.select('title/text()'))

        url = self.get_or_none(node.select('link/text()'))
        description = self.get_or_none(node.select('description/text()'))
        pub_date = self.get_or_none(node.select('pubDate/text()'))
        category = self.get_or_none(node.select('category/text()'))
        # image = node.select('item/media:content/url')

        item = {}
        item['title'] = title
        item['url'] = url

        item['pub_date'] = pub_date
        item['category'] = category
        item['description'] = description
        item['domain'] = get_domain(response.url)
        return item
