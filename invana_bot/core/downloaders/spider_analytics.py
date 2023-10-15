class IndividualSpiderRequestStats(object):
    """
    To calculate the spider stats
    """
    def process_request(self, request, spider):
        spider_id = spider.spider_config.get("spider_id")
        spider.crawler.stats.inc_value('invana-stats/{}/requests_count'.format(spider_id), spider=spider)


class IndividualSpiderResponseStats(object):
    """
    To calculate the spider stats
    """

    def process_response(self, request, response, spider):
        spider_id = spider.spider_config.get("spider_id")
        spider.crawler.stats.inc_value('invana-stats/{}/responses_count'.format(spider_id), spider=spider)
        return response
