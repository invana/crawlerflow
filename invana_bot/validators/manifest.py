import yaml

DOCUMENTATION_URL = "https://invanalabs.github.io/invana-bot/spiders/manifest/"


class InvanaBotManifestItemBase(object):
    REQUIRED_FIELDS = []
    VALIDATOR_NAME = None

    def __init__(self, data=None):
        self.validate(data=data)

    def setup(self, data=None):
        raise NotImplementedError()

    def _validate_required_keys(self, data=None):
        data_keys = data.keys()
        errors = []
        for required_field in self.REQUIRED_FIELDS:
            if required_field not in data_keys:
                errors.append("{} key not defined in the {}".format(required_field, self.VALIDATOR_NAME))
        return errors

    def validate(self, data=None):
        errors = self._validate_required_keys(data=data)
        if errors.__len__() == 0:
            self.setup(data=data)
        return self, errors


class ManifestValidator(object):
    """

    """

    REQUIRED_KEYS = ("cti_id", "init_spider", "spiders", "settings", "context")

    def validate_manifest(self, manifest=None):
        """

        :param manifest: in json format.
        :return: (Manifest instance, errors)
        """
        errors = []
        manifest_keys = manifest.items()
        for required_key in self.REQUIRED_KEYS:
            if required_key not in manifest_keys:
                errors.append("{} key not defined in the manifest")

        self.validate_init_spider(data=manifest.get("init_spider", None))

        for spider in manifest.get("init_spider", []):
            pass
        return self, errors

    def validate_init_spider(self, data=None):
        errors = []
        if data is None:
            errors.append("init_spider cannot be None. Refer documentation at {}".format(DOCUMENTATION_URL))

        return InvanaBotInitSpider(data=data), errors

    def validate_spiders(self):
        return self.settings

    def validate_settings(self):
        return self.context

    def validate_context(self):
        return self.context


class InvanaBotInitSpider(InvanaBotManifestItemBase):
    spider_id = None
    start_urls = []
    REQUIRED_FIELDS = ["spider_id", "start_urls"]
    VALIDATOR_NAME = "init_spider"

    def setup(self, data=None):
        self.spider_id = data.get("spider_id")
        self.start_urls = data.get("start_urls", [])


class InvanaBotSettings(object):
    allowed_domains = []
    download_delay = 0
    data_storage = []

    def get_data_storages(self):
        return self.data_storage


class InvanaBotSpider(InvanaBotManifestItemBase):
    spider_id = None
    allowed_domains = None
    extractors = []
    traversals = []

    REQUIRED_FIELDS = ["spider_id", "allowed_domains", "extractors", "traversals"]
    VALIDATOR_NAME = "spider"

    def get_data_schema(self):
        # this method works only for CustomExtractor where data types are specified.
        pass


class InvanaBotTraversal(object):
    traversal_id = None
    selector_type = None
    selector_value = None
    max_pages = None
    next_spider_id = None


class InvanaBotExtractor(object):
    extractor_id = None
    extractor_type = None
    data_selectors = []


class InvanaBotDataSelector(object):
    selector_id = None
    selector = None
    selector_type = None
    selector_attribute = None
    data_type = None


class InvanaBotDataStorage(object):
    storage_id = None
    storage_type = None
    connection_uri = None
    database_name = None
    collection_name = None
    unique_key = None
