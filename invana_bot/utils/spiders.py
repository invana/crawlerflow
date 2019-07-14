def get_crawler_from_list(spiders=None, spider_id=None):
    for crawler in spiders:
        if crawler.get("spider_id") == spider_id:
            return crawler
    raise Exception("spider_id: {} not found in the spiders data".format(spider_id))
