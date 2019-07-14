class ExtractorBase(object):
    """




    """

    def __init__(self, response=None, extractor=None, extractor_id=None):
        """
        :param response: html response of the request
        :param extractor: extractor configuration in json.
        :param extractor_id:
        """
        if None in [response, extractor, extractor_id]:
            raise Exception("Invalid input to the extractor class, response, extractor and extractor_id are mandatory")
        self.response = response
        self.extractor = extractor
        self.extractor_id = extractor_id
