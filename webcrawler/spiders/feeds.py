from scrapy.spiders import XMLFeedSpider


class GenericFeedSpider(XMLFeedSpider):
    name = "generic_feed_spider"
    itertag = 'item'
    iterator = 'iternodes'  # This is actually unnecessary, since it's the default value

    def parse_node(self, response, node):
        print("Parse node ===================")
        title = node.select('title/text()').extract_first()
        url = node.select('link/text()').extract_first()
        description = node.select('description/text()').extract_first()
        pub_date = node.select('pubDate/text()').extract_first()
        category = node.select('category/text()').extract_first()
        # image = node.select('item/media:content/url').extract_first()

        item = {}
        item['title'] = title
        item['url'] = url
        item['pub_date'] = pub_date
        item['category'] = category
        item['description'] = description
        print(item)
        return item
