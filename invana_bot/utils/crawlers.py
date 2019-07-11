def get_crawler_from_list(crawlers=None, crawler_id=None):
    for crawler in crawlers:
        if crawler.get("crawler_id") == crawler_id:
            return crawler
    raise Exception("crawler_id: {} not found in the spiders data".format(crawler_id))
