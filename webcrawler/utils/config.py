from webcrawler.exceptions import NotImplemented, InvalidCrawlerConfig


def validate_config(config=None):
    required_keys = ['crawler_name', 'domain', 'subdomain', 'start_url', 'data_selectors']
    for key_ in required_keys:
        if key_ not in config.keys():
            InvalidCrawlerConfig("Invalid configuration: Required Key {0} not found in the configuration".format(key_))
    # TODO - validate all the data_selectors data aswell
    return True


def process_config(config=None):
    processed_config_dict = {}
    parent_selectors = []
    new_config_selectors = []
    for selector in config['data_selectors']:
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
    for selector in config['data_selectors']:
        if selector.get('parent_selector') is None and selector.get('selector_attribute') != 'element':
            new_config_selectors.append(selector)

    for k, v in processed_config_dict.items():
        new_config_selectors.append(v)
    config['data_selectors'] = new_config_selectors
    return config
