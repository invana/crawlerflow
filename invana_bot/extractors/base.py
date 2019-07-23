class ExtractorBase(object):
    """




    """

    def __init__(self, response=None, extractor=None, extractor_id=None, extractor_fn=None):
        """
        :param response: html response of the request
        :param extractor: extractor configuration in json; this is optional in most cases.
        :param extractor_fn: extractor python lambda; this is optional in most cases.
        :param extractor_id: the field with which data is stored in database.
        """
        if None in [response, extractor, extractor_id]:
            raise Exception("Invalid input to the extractor class, response, extractor and extractor_id are mandatory")
        self.response = response
        self.extractor = extractor
        self.extractor_id = extractor_id
        self.extractor_fn = extractor_fn
