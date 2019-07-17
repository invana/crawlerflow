from invana_bot.utils.exceptions import InvalidCrawlerConfig


def validate_config(config=None):
    required_keys = ['start_url', 'data_selectors']
    for key_ in required_keys:
        if key_ not in config.keys():
            raise InvalidCrawlerConfig(
                "Invalid configuration: Required Key {0} not found in the configuration".format(key_))
    # TODO - validate all the data_selectors data aswell
    return True


class InvanaBotConfigValidator(object):

    CRAWLER_EXAMPLE = {
        "spider_id": "blogs_list",
        "extractors": [],
        "traversals": []
    }
    PARSER_EXAMPLE = {
        "extractor_type": "CustomContentExtractor",
        "extractor_id": "example_parser",
        "data_selectors": []
    }
    all_errors = []

    def __init__(self, config=None, spider_type="web"):
        self.config = config
        self.spider_type = spider_type

    def log_error(self, error_text):
        self.all_errors.append(error_text)

    def validate_required_fields(self):
        required_keys = ['cti_id', 'init_spider', 'spiders']
        for key_ in required_keys:
            if key_ not in self.config.keys():
                self.log_error(
                    "Invalid configuration: Required Key {0} not found in the configuration".format(key_))
        # TODO - validate all the data_selectors data aswell
        # print("all the required fields exist")
        return True

    # @staticmethod
    # def validate_options_fields():
    #     optional_keys = ['transformations', 'data_storages', 'callbacks', 'context']
    #

    def validate_selector(self, selector=None):

        selector_attribute = selector.get("selector_attribute")
        if selector_attribute is None:
            raise InvanaBotConfigValidator("field 'selector_attribute' is mandatory for selector object")

        selector_keys = selector.keys()
        if selector_attribute == "element":
            required_fields = ["selector_id", "selector", "child_selectors", "selector_attribute"]
            for field in required_fields:
                if field not in selector_keys:
                    self.log_error(
                        "{} field not found in 'selector_attribute={}' type selector".format(field, selector_attribute))

        else:
            required_fields = ["selector_id", "selector", "selector_type", "selector_attribute"]

            for field in required_fields:
                if field not in selector_keys:
                    self.log_error(
                        "{} field not found in 'selector_attribute!={}' type selector".format(field,
                                                                                              selector_attribute))

    def validate_spiders(self, spiders=None):
        # print(spiders)

        spider_required_fields = [
            {
                "extractor_id": "spider_id",
                "field_type": str
            },
            # {
            #     "extractor_id": "extractors",
            #     "field_type": list
            # }

        ]

        required_extractors_fields = [
            {
                "extractor_id": "extractor_type",
                "field_type": str
            }
        ]

        for spider in spiders:
            spider_config_keys = spider.keys()
            # check if all required keys where there.
            for required_field in spider_required_fields:
                if required_field['extractor_id'] in spider_config_keys:
                    pass
                else:
                    self.log_error(
                        "required field '{}' in spiders data not found".format(required_field['extractor_id']))

                if type(spider[required_field['extractor_id']]) is not required_field['field_type']:
                    self.log_error(
                        "required field '{}' in spiders should of '{}' data type".format(required_field['extractor_id'],
                                                                                          required_field['field_type']))

            """
            making sure extractors data is correct
            """
            for required_field in required_extractors_fields:
                for parser in spider.get('extractors',[]):
                    parser_config_keys = parser.keys()
                    if required_field['extractor_id'] in parser_config_keys:
                        pass
                    else:
                        self.log_error(
                            "required field '{}' in parser data not found".format(required_field['extractor_id']))

                    if type(parser[required_field['extractor_id']]) is not required_field['field_type']:
                        self.log_error(
                            "required field '{}' in extractors should of '{}' data type".format(
                                required_field['extractor_id'],
                                required_field['field_type']))

                    if parser['extractor_type'] == "CustomContentExtractor":
                        if len(parser.get('data_selectors', [])) == 0:
                            self.log_error(
                                "data_selectors should be specified when using extractor_type 'CustomContentExtractor'")

                    data_selectors = parser.get("data_selectors", [])
                    for selector in data_selectors:
                        pass  # TODO - implement data selector validations.
                        self.validate_selector(selector=selector)

            traversals = spider.get('traversals', [])
            if type(traversals) is not list:
                self.log_error(
                    "traversals data in the spider '{}' should be of list type".format(spider['spider_id']))

            self.validate_traversals(traversals=traversals, spider=spider, all_spiders=spiders)

    def validate_traversals(self, traversals=None, spider=None, all_spiders=None):

        must_have_keys = ["traversal_id", "selector_type", "selector_value", ]
        all_spiders_ids = [spider['spider_id'] for spider in all_spiders]

        for traversal in traversals:
            next_spider_id = traversal.get("next_spider_id")

            traversal_example = """
            
Here are examples of traversal

# css
{
    "traversal_id": "xyz_pagination",
    "selector_type": "css",
    "selector_value": "h1",
    "max_pages": 100,
    "next_spider_id": "blogs_list"
}  

# xpath
{
    "traversal_id": "xyz_pagination",
    "selector_type": "xpath",
    "selector_value": "//title",
    "max_pages": 100,
    "next_spider_id": "blogs_list"
}       

# regex
{
    "traversal_id": "xyz_pagination",
    "selector_type": "regex",
    "selector_value": "*/blog/*",
    "max_pages": 100,
    "next_spider_id": "blogs_list"
}            
            
            """

            if next_spider_id is None:
                self.log_error("All Traversals should have next_spider_id set  {}".format(traversal_example))

            if next_spider_id not in all_spiders_ids:
                self.log_error("You are using next_spider_id '{}' "
                               "but it is not defined in the spiders."
                               " Available spider_id in the config are {} {}".format(next_spider_id,
                                                                                      all_spiders_ids,
                                                                                      traversal_example))

    def validate_transformations_and_data_storages(self):
        transformations = self.config.get('transformations', [])
        data_storages = self.config.get('data_storages', [])
        if len(data_storages) == 0:
            if len(transformations) > 0:
                self.log_error("transformations cannot be applied if data_storages is not defined.")
            # print("Ignoring the transformation if index")
        else:
            transformation_ids = [transformation.get('transformation_id') for transformation in transformations]

            for transformation in transformations:
                transformation_id = transformation.get("transformation_id")
                transformation_fn = transformation.get("transformation_fn")
                if transformation_fn is None:
                    self.log_error("transformation with transformation_id "
                                   "'{}' doesn't have transformation_fn set".format(transformation_id))

            example_index = {
                "transformation_id": "default",
                "connection_uri": "mongodb://127.0.0.1/spiders_data_index",
                "collection_name": "blogs_list",
                "unique_key": "url"
            }
            # transformation_ids_in_data_storages = [index.get('transformation_id') for index in data_storages]
            index_required_fields = example_index.keys()
            for index in data_storages:
                transformation_id = index.get("transformation_id")
                for required_field in index_required_fields:
                    if index.get(required_field) is None:
                        self.log_error("required field '{}' is missing in the index configuration."
                                       " Example is {} ".format(required_field, example_index))

                if transformation_id not in transformation_ids:
                    self.log_error("index with transformation_id '{}' has no"
                                   " transformation defined in transformations".format(transformation_id))

    def validate_callback(self):
        all_data_storage_ids = [index.get('data_storage_id') for index in self.config.get("data_storages", [])]

        callback_template = {
            "callback_id": "default",
            "data_storage_id": "default",
            "url": "http://localhost/api/callback",
            "request_type": "POST",
            "payload": {
            },
            "headers": {
                "X-TOKEN": "abc123456789"
            }
        }

        callbacks = self.config.get("callbacks", [])
        callback_required_keys = callback_template.keys()
        for callback in callbacks:
            callback_id = callback.get("callback_id")
            callback_data_storage_id = callback.get("data_storage_id")
            if callback_id is None:
                self.log_error("Invalid callback configuration, callback_id cannot be None."
                               " Here is the example {}".format(callback_template))

            if callback_data_storage_id not in all_data_storage_ids:
                self.log_error("callback is set with an index - '{}' which is not "
                               "defined in the data_storages configuration."
                               "".format(callback_data_storage_id))

            for required_field in callback_required_keys:
                if callback.get(required_field) is None:
                    self.log_error("Required key {} missing in callback_id '{}' "
                                   "".format(required_field, callback_id))

    def validate_settings(self):
        settings = self.config.get("settings", {})
        required_keys = [ 'allowed_domains']
        for required_key in required_keys:
            if required_key not in settings.keys():
                self.log_error(
                    "required field '{}' in settings data not found".format(required_key))

    def validate(self):
        self.validate_required_fields()
        self.validate_spiders(spiders=self.config['spiders'])
        self.validate_transformations_and_data_storages()
        self.validate_callback()
        self.validate_settings()
        return self.all_errors


# def validate_cti_config(config=None):
#     optional_keys = ['transformations', 'data_storages', 'callbacks']
#     required_keys = ['cti_id', 'init_spider', 'spiders']
#     for key_ in required_keys:
#         if key_ not in config.keys():
#             raise InvalidCrawlerConfig(
#                 "Invalid configuration: Required Key {0} not found in the configuration".format(key_))
#     # TODO - validate all the data_selectors data aswell
#     return True


# def process_config(config=None):
#     processed_config_dict = {}
#     parent_selectors = []
#     new_config_selectors = []
#     for selector in config.get('data_selectors', []):
#         if selector.get('selector_attribute') == 'element':
#             parent_selectors.append(selector)
#
#     """
#     process the element root selectors (without parent_selector) which might become dictionaries
#     """
#     if len(parent_selectors) > 0:
#         for parent_selector in parent_selectors:
#             processed_config_dict[parent_selector.get('id')] = parent_selector
#             processed_config_dict[parent_selector.get('id')]['child_selectors'] = []
#
#             for selector in config['data_selectors']:
#                 if selector.get('parent_selector') == parent_selector.get('id'):
#                     processed_config_dict[parent_selector.get('id')]['child_selectors'].append(selector)
#
#     """
#     process the elements with no root selectors
#     """
#     for selector in config.get('data_selectors', []):
#         if selector.get('parent_selector') is None and selector.get('selector_attribute') != 'element':
#             new_config_selectors.append(selector)
#
#     for k, v in processed_config_dict.items():
#         new_config_selectors.append(v)
#     config['data_selectors'] = new_config_selectors
#     return config


def validate_cti_config(cti_manifest):
    validator = InvanaBotConfigValidator(config=cti_manifest)
    errors = validator.validate()
    return errors


def validate_spider_config(spider_config):
    # TODO - fix this validations for spider config later.
    return []
