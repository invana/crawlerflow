from invana_bot.exceptions import InvalidCrawlerConfig


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
        "parser_name": "CustomContentExtractor",
        "data_selectors": []
    }

    def __init__(self, config=None):
        self.config = config

    def validate_required_fields(self):
        required_keys = ['cti_id', 'init_data', 'crawlers']
        for key_ in required_keys:
            if key_ not in self.config.keys():
                raise InvalidCrawlerConfig(
                    "Invalid configuration: Required Key {0} not found in the configuration".format(key_))
        # TODO - validate all the data_selectors data aswell
        print("all the required fields exist")
        return True

    def validate_options_fields(self):
        optional_keys = ['transformations', 'indexes', 'callbacks', 'context']

    def validate_selector(self, selector=None):

        selector_attribute = selector.get("selector_attribute")
        if selector_attribute is None:
            raise InvanaBotConfigValidator("field 'selector_attribute' is mandatory for selector object")

        selector_keys = selector.keys()
        if selector_attribute == "element":
            required_fields = ["id", "selector", "child_selectors", "selector_attribute"]
            for field in required_fields:
                if field not in selector_keys:
                    raise InvalidCrawlerConfig(
                        "{} field not found in 'selector_attribute={}' type selector".format(field, selector_attribute))

        else:
            required_fields = ["id", "selector", "selector_type", "selector_attribute"]

            for field in required_fields:
                if field not in selector_keys:
                    raise InvalidCrawlerConfig(
                        "{} field not found in 'selector_attribute!={}' type selector".format(field,
                                                                                              selector_attribute))

    def validate_crawlers(self, crawlers=None):
        print(crawlers)
        crawler_required_fields = [
            {
                "field_name": "crawler_id",
                "field_type": str
            },
            {
                "field_name": "parsers",
                "field_type": list
            }

        ]

        required_parsers_fields = [
            {
                "field_name": "parser_name",
                "field_type": str
            }
        ]

        for crawler in crawlers:
            crawler_config_keys = crawler.keys()
            # check if all required keys where there.
            for required_field in crawler_required_fields:
                if required_field['field_name'] in crawler_config_keys:
                    pass
                else:
                    raise InvalidCrawlerConfig(
                        "required field '{}' in crawlers data not found".format(required_field['field_name']))

                if type(crawler[required_field['field_name']]) is not required_field['field_type']:
                    raise InvalidCrawlerConfig(
                        "required field '{}' in crawlers should of '{}' data type".format(required_field['field_name'],
                                                                                          required_field['field_type']))

            """
            making sure parsers data is correct
            """
            for required_field in required_parsers_fields:
                for parser in crawler['parsers']:
                    parser_config_keys = parser.keys()
                    if required_field['field_name'] in parser_config_keys:
                        pass
                    else:
                        raise InvalidCrawlerConfig(
                            "required field '{}' in parser data not found".format(required_field['field_name']))

                    if type(parser[required_field['field_name']]) is not required_field['field_type']:
                        raise InvalidCrawlerConfig(
                            "required field '{}' in parsers should of '{}' data type".format(
                                required_field['field_name'],
                                required_field['field_type']))

                    if parser['parser_name'] == "CustomContentExtractor":
                        if len(parser.get('data_selectors', [])) == 0:
                            raise InvalidCrawlerConfig(
                                "data_selectors should be specified when using parser_name 'CustomContentExtractor'")

                    data_selectors = parser.get("data_selectors", [])
                    for selector in data_selectors:
                        pass  # TODO - implement data selector validations.
                        self.validate_selector(selector=selector)

            traversals = crawler.get('traversals', [])
            if type(traversals) is not list:
                raise InvalidCrawlerConfig(
                    "traversals data in the crawler '{}' should be of list type".format(crawler['crawler_id']))

            self.validate_traversals(traversals=traversals, crawler=crawler, all_crawlers=crawlers)

    def validate_traversals(self, traversals=None, crawler=None, all_crawlers=None):
        valid_traversal_types = ['pagination', 'same_domain', 'link_from_field']

        all_crawlers_ids = [crawler['crawler_id'] for crawler in all_crawlers]

        for traversal in traversals:
            traversal_type = traversal.get("traversal_type")
            if traversal_type not in valid_traversal_types:
                raise InvalidCrawlerConfig("Traversal of types '{}' are accepted, where as you have "
                                           " traversal_type '{}'".format(", ".join(valid_traversal_types),
                                                                         traversal_type))

            if traversal_type not in traversal.keys():
                raise InvalidCrawlerConfig("Traversal of type '{}' should have '{}' key defining the"
                                           " traversal configuration ".format(traversal_type, traversal_type))
            next_crawler_id = traversal.get("next_crawler_id")

            if next_crawler_id is None:
                raise InvalidCrawlerConfig("All Traversals should have next_crawler_id set ")

            if next_crawler_id not in all_crawlers_ids:
                raise InvalidCrawlerConfig("You are using next_crawler_id '{}' "
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
                        raise InvalidCrawlerConfig(
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
                        "parser_name": "CustomContentExtractor",
                        "field_name": "url"
                    },
                    "next_crawler_id": "blog-detail"
                }
                required_fields = ['parser_name', 'field_name']
                for required_field in required_fields:
                    if required_field in traversal[traversal_type].keys():
                        raise InvalidCrawlerConfig(
                            "Traversal type '{}' in crawler '{}' should have the config "
                            "with keys '{}' along with optional max_pages. Example: {}"
                            "".format(
                                traversal_type,
                                crawler['crawler_id'],
                                ", ".join(required_fields), traversal_example))

    def validate(self):
        self.validate_required_fields()
        self.validate_crawlers(crawlers=self.config['crawlers'])


def validate_cti_config(config=None):
    optional_keys = ['transformations', 'indexes', 'callbacks']
    required_keys = ['cti_id', 'init_data', 'crawlers']
    for key_ in required_keys:
        if key_ not in config.keys():
            raise InvalidCrawlerConfig(
                "Invalid configuration: Required Key {0} not found in the configuration".format(key_))
    # TODO - validate all the data_selectors data aswell
    return True


def process_config(config=None):
    processed_config_dict = {}
    parent_selectors = []
    new_config_selectors = []
    for selector in config.get('data_selectors', []):
        if selector.get('selector_attribute') == 'element':
            parent_selectors.append(selector)

    """
    process the element root selectors (without parent_selector) which might become dictionaries
    """
    if len(parent_selectors) > 0:
        for parent_selector in parent_selectors:
            processed_config_dict[parent_selector.get('id')] = parent_selector
            processed_config_dict[parent_selector.get('id')]['child_selectors'] = []

            for selector in config['data_selectors']:
                if selector.get('parent_selector') == parent_selector.get('id'):
                    processed_config_dict[parent_selector.get('id')]['child_selectors'].append(selector)

    """
    process the elements with no root selectors
    """
    for selector in config.get('data_selectors', []):
        if selector.get('parent_selector') is None and selector.get('selector_attribute') != 'element':
            new_config_selectors.append(selector)

    for k, v in processed_config_dict.items():
        new_config_selectors.append(v)
    config['data_selectors'] = new_config_selectors
    return config
