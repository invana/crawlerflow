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
        "crawler_id": "blogs_list",
        "parsers": [],
        "traversals": []
    }
    PARSER_EXAMPLE = {
        "parser_type": "CustomContentExtractor",
        "parser_id": "example_parser",
        "data_selectors": []
    }
    all_errors = []

    def __init__(self, config=None):
        self.config = config

    def log_error(self, error_text):
        self.all_errors.append(error_text)

    def validate_required_fields(self):
        required_keys = ['cti_id', 'init_crawler', 'crawlers']
        for key_ in required_keys:
            if key_ not in self.config.keys():
                self.log_error(
                    "Invalid configuration: Required Key {0} not found in the configuration".format(key_))
        # TODO - validate all the data_selectors data aswell
        # print("all the required fields exist")
        return True

    # @staticmethod
    # def validate_options_fields():
    #     optional_keys = ['transformations', 'indexes', 'callbacks', 'context']
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

    def validate_crawlers(self, crawlers=None):
        # print(crawlers)
        crawler_required_fields = [
            {
                "parser_id": "crawler_id",
                "field_type": str
            },
            {
                "parser_id": "parsers",
                "field_type": list
            }

        ]

        required_parsers_fields = [
            {
                "parser_id": "parser_type",
                "field_type": str
            }
        ]

        for crawler in crawlers:
            crawler_config_keys = crawler.keys()
            # check if all required keys where there.
            for required_field in crawler_required_fields:
                if required_field['parser_id'] in crawler_config_keys:
                    pass
                else:
                    self.log_error(
                        "required field '{}' in crawlers data not found".format(required_field['parser_id']))

                if type(crawler[required_field['parser_id']]) is not required_field['field_type']:
                    self.log_error(
                        "required field '{}' in crawlers should of '{}' data type".format(required_field['parser_id'],
                                                                                          required_field['field_type']))

            """
            making sure parsers data is correct
            """
            for required_field in required_parsers_fields:
                for parser in crawler['parsers']:
                    parser_config_keys = parser.keys()
                    if required_field['parser_id'] in parser_config_keys:
                        pass
                    else:
                        self.log_error(
                            "required field '{}' in parser data not found".format(required_field['parser_id']))

                    if type(parser[required_field['parser_id']]) is not required_field['field_type']:
                        self.log_error(
                            "required field '{}' in parsers should of '{}' data type".format(
                                required_field['parser_id'],
                                required_field['field_type']))

                    if parser['parser_type'] == "CustomContentExtractor":
                        if len(parser.get('data_selectors', [])) == 0:
                            self.log_error(
                                "data_selectors should be specified when using parser_type 'CustomContentExtractor'")

                    data_selectors = parser.get("data_selectors", [])
                    for selector in data_selectors:
                        pass  # TODO - implement data selector validations.
                        self.validate_selector(selector=selector)

            traversals = crawler.get('traversals', [])
            if type(traversals) is not list:
                self.log_error(
                    "traversals data in the crawler '{}' should be of list type".format(crawler['crawler_id']))

            self.validate_traversals(traversals=traversals, crawler=crawler, all_crawlers=crawlers)

    def validate_traversals(self, traversals=None, crawler=None, all_crawlers=None):
        valid_traversal_types = ['pagination', 'same_domain', 'link_from_field']

        all_crawlers_ids = [crawler['crawler_id'] for crawler in all_crawlers]

        for traversal in traversals:
            traversal_type = traversal.get("traversal_type")
            if traversal_type not in valid_traversal_types:
                self.log_error("Traversal of types '{}' are accepted, where as you have "
                               " parser_id '{}'".format(", ".join(valid_traversal_types),
                                                          traversal_type))

            if traversal_type not in traversal.keys():
                self.log_error("Traversal of type '{}' should have '{}' key defining the"
                               " traversal configuration ".format(traversal_type, traversal_type))
            next_crawler_id = traversal.get("next_crawler_id")

            if next_crawler_id is None:
                self.log_error("All Traversals should have next_crawler_id set ")

            if next_crawler_id not in all_crawlers_ids:
                self.log_error("You are using next_crawler_id '{}' "
                               "but it is not defined in the crawlers."
                               " Available crawler_id in the config are {}".format(next_crawler_id,
                                                                                   all_crawlers_ids))

            if traversal_type == "pagination":
                required_fields = ['selector', 'selector_type']
                traversal_example = {
                    "traversal_type": "pagination",
                    "pagination": {
                        "sel ector": ".next-posts-link",
                        "selector_type": "css",
                        "max_pages": 4
                    },
                    "next_crawler_id": "blogs_list"
                }
                for required_field in required_fields:
                    if required_field not in traversal[traversal_type].keys():
                        self.log_error(
                            "Traversal type '{}' in crawler '{}' should have the config with keys '{}' along with optional max_pages."
                            " Example: {}"
                            "".format(
                                traversal_type,
                                crawler['crawler_id'],
                                ", ".join(required_fields), traversal_example))

            elif traversal_type == "same_domain":
                pass  # don't have any required fields.

            elif traversal_type == "link_from_field":
                traversal_example = {
                    "traversal_type": "link_from_field",
                    "link_from_field": {
                        "parser_id": "blog_list_parser",
                        "selector_id": "url"
                    },
                    "next_crawler_id": "blog-detail"
                }
                required_fields = ['parser_id', 'selector_id']
                for required_field in required_fields:
                    if required_field not in traversal[traversal_type].keys():
                        self.log_error(
                            "Traversal type '{}' in crawler '{}' should have the config "
                            "with keys '{}' along with optional max_pages. Example: {}"
                            "".format(
                                traversal_type,
                                crawler['crawler_id'],
                                ", ".join(required_fields), traversal_example))

    def validate_transformations_and_indexes(self):
        transformations = self.config.get('transformations', [])
        indexes = self.config.get('indexes', [])
        if len(indexes) == 0:
            if len(transformations) > 0:
                self.log_error("transformations cannot be applied if indexes is not defined.")
            print("Ignoring the transformation if index")
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
                "connection_uri": "mongodb://127.0.0.1/crawlers_data_index",
                "collection_name": "blogs_list",
                "unique_key": "url"
            }
            # transformation_ids_in_indexes = [index.get('transformation_id') for index in indexes]
            index_required_fields = example_index.keys()
            for index in indexes:
                transformation_id = index.get("transformation_id")
                for required_field in index_required_fields:
                    if index.get(required_field) is None:
                        self.log_error("required field '{}' is missing in the index configuration."
                                       " Example is {} ".format(required_field, example_index))

                if transformation_id not in transformation_ids:
                    self.log_error("index with transformation_id '{}' has no"
                                   " transformation defined in transformations".format(transformation_id))

    def validate_callback(self):
        all_index_ids = [index.get('index_id') for index in self.config.get("indexes", [])]

        callback_template = {
            "callback_id": "default",
            "index_id": "default",
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
            callback_index_id = callback.get("index_id")
            if callback_id is None:
                self.log_error("Invalid callback configuration, callback_id cannot be None."
                               " Here is the example {}".format(callback_template))

            if callback_index_id not in all_index_ids:
                self.log_error("callback is set with an index - '{}' which is not "
                               "defined in the indexes configuration."
                               "".format(callback_index_id))

            for required_field in callback_required_keys:
                if callback.get(required_field) is None:
                    self.log_error("Required key {} missing in callback_id '{}' "
                                   "".format(required_field, callback_id))

    def validate_settings(self):
        settings = self.config.get("settings", {})
        required_keys = ['download_delay', 'allowed_domains']
        for required_key in required_keys:
            if required_key not in settings.keys():
                self.log_error(
                    "required field '{}' in settings data not found".format(required_key))

    def validate(self):
        self.validate_required_fields()
        self.validate_crawlers(crawlers=self.config['crawlers'])
        self.validate_transformations_and_indexes()
        self.validate_callback()
        self.validate_settings()
        return self.all_errors


# def validate_cti_config(config=None):
#     optional_keys = ['transformations', 'indexes', 'callbacks']
#     required_keys = ['cti_id', 'init_crawler', 'crawlers']
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


def validate_crawler_config(crawler_config):
    # TODO - fix this validations for crawler config later.
    return []
