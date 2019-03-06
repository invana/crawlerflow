
def get_crawler_from_list(crawlers=None, crawler_id=None):
    for parser in crawlers:
        if parser.get("crawler_id") == crawler_id:
            return parser
    return