from scrapy.linkextractors import LinkExtractor


class GenericLinkExtractor(object):
    """


    """

    def __init__(self,
                 restrict_xpaths=(),
                 restrict_css=(),
                 restrict_regex=(),
                 allow_domains=(),
                 link_extractor_cls=LinkExtractor, **kwargs):
        """

        :param restrict_xpaths: list of xpaths for links Extraction.
        :param restrict_css: list of xpath for links extraction
        :param restrict_regex: list of regex patterns
        :param link_extractor_cls: defaults to scrapy link extractor
        :param allow_domains: defaults to the allowed domains of spider
        """
        self.restrict_xpaths = restrict_xpaths
        self.restrict_css = restrict_css
        self.restrict_regex = restrict_regex
        self.allow_domains = allow_domains
        self.link_extractor_cls = link_extractor_cls

    def extract_links(self, response=None):
        all_links = self.link_extractor_cls(allow=self.restrict_xpaths,
                                            restrict_xpaths=self.restrict_xpaths,
                                            restrict_css=self.restrict_css,
                                            allow_domains=self.allow_domains
                                            ).extract_links(response=response)
        return [link.url for link in all_links]
