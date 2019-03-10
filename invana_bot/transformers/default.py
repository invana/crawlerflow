def default_transformer(results):
    results_cleaned = results
    return results_cleaned


class InvanaBotTranformerBase(object):

    def __init__(self, cti_config=None,
                 transformer_name=None,
                 cit_id=None,
                 crawled_id=None,
                 job_id=None):

        if None in [transformer_name,
                    cit_id, crawled_id, job_id]:
            raise Exception("transformer_name, cit_id, crawled_id, job_id "
                            "should be given as input for InvanaBotTranformer ")
        self.cti_config = cti_config
        self.transformer_name = transformer_name
        self.cit_id = cit_id
        self.crawled_id = crawled_id
        self.job_id = job_id

    def transform(self):
        raise NotImplementedError("this method should be implemented")

    def filter_data(self):
        pass
