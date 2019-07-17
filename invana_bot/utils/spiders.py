def get_spider_from_list(spiders=None, spider_id=None):
    for spider in spiders:
        if spider.get("spider_id") == spider_id:
            return spider
    raise Exception("spider_id: {} not found in the spiders data".format(spider_id))
