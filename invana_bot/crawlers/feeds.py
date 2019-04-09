# from scrapy.spiders import XMLFeedSpider, Spider
# from invana_bot.utils.url import get_domain
# import feedparser
#
#
# class GenericFeedSpider(XMLFeedSpider):
#     name = "generic_feed_spider"
#     itertag = 'item'
#     iterator = 'xml'  # This is actually unnecessary, since it's the default value
#
#     def get_or_none(self, selector):
#         try:
#             return selector.extract_first()
#         except Exception as e:
#             print(e)
#             return None
#
#     def parse_node(self, response, node):
#         title = self.get_or_none(node.select('title/text()'))
#
#         url = self.get_or_none(node.select('link/text()'))
#         description = self.get_or_none(node.select('description/text()'))
#         pub_date = self.get_or_none(node.select('pubDate/text()'))
#         category = self.get_or_none(node.select('category/text()'))
#         # image = node.select('item/media:content/url')
#
#         item = {}
#         item['title'] = title
#         item['url'] = url
#
#         item['pub_date'] = pub_date
#         item['category'] = category
#         item['description'] = description
#         item['domain'] = get_domain(response.url)
#         return item
#
#
# class RSSSpider(Spider):
#     """
#
#     https://gist.github.com/nyov/9c70e780ea80204559d6da5525228702
#
#     """
#     name = "rss"
#
#     def parse_feed(self, feed):
#         """ Parse RSS/Atom feed using feedparser
#         """
#         data = feedparser.parse(feed)
#         if data.bozo:
#             if (hasattr(data.bozo_exception, 'getLineNumber') and
#                     hasattr(data.bozo_exception, 'getMessage')):
#                 line = data.bozo_exception.getLineNumber()
#                 # segment = feed.split('\n')[line - 1]
#             # could still try to return data. not necessarily completely broken
#             return None
#         return data
#
#     def parse(self, response):
#         # parse downloaded content with feedparser (NOT re-downloading with feedparser)
#         feed = self.parse_feed(response.body)
#         if feed:
#             # grab some feed elements
#             # - https://pythonhosted.org/feedparser/common-rss-elements.html
#             # - https://pythonhosted.org/feedparser/common-atom-elements.html
#
#             # ns = feed.namespaces
#             # feed_title = feed.feed.title
#             # feed_link = feed.feed.link
#             # feed_desc = feed.feed.description
#
#             for entry in feed.entries:
#                 # have content?
#                 content = entry.get('content')
#                 if content:
#                     # content = content[0]
#                     content = content[0]['value']
#
#                 item = {
#                     # global feed data
#                     # 'feed_title': feed_title,
#                     # 'feed_link': feed_link,
#                     # 'feed_description': feed_desc,
#                     #
#                     # item entry data
#                     # 'url': response.url,
#                     'url': entry.link,
#                     'title': entry.title,
#                     'domain': get_domain(response.url),
#                     'description': entry.description,
#                     # 'date': entry.published,
#                     # 'date': entry.published_parsed,
#                     'pub_date': entry.updated_parsed,
#
#                     # optional
#                     'content': content,
#                     'type': entry.get('dc_type'),
#                 }
#
#                 yield item
