def clean_data(elems=None, selector=None):
    if selector.get('multiple'):
        data_cleaned = []
        data = elems.extract()
        for i, datum in enumerate(data):
            if datum:
                data_cleaned.append(datum.strip())
        return data_cleaned
    else:
        data = elems.extract_first()
        if data:
            return data.strip()
        return data


def get_selector_element(html_element, selector, ):
    if selector.get('selector_attribute') in ['text']:
        if selector.get('selector_type') == 'css':
            elems = html_element.css("{0}::{1}".format(selector.get('selector'),
                                                       selector.get('selector_attribute')))
            return clean_data(elems=elems, selector=selector)
        else:
            elems = html_element.xpath("{0}/{1}".format(selector.get('selector'),
                                                        selector.get('selector_attribute')))
            return clean_data(elems=elems, selector=selector)
    elif selector.get('selector_attribute') == 'html':
        if selector.get('selector_type') == 'css':
            elems = html_element.css(selector.get('selector'))
            return clean_data(elems=elems, selector=selector)
        else:
            elems = html_element.xpath("{0}/{1}".format(selector.get('selector'),
                                                        selector.get('selector_attribute')))
            return clean_data(elems=elems, selector=selector)
    else:
        if selector.get('selector_type') == 'css':
            elems = html_element.css(selector.get('selector')) \
                .xpath("@{0}".format(selector.get('selector_attribute')))
            return clean_data(elems=elems, selector=selector)
        else:
            elems = html_element.xpath("{0}/{1}".format(selector.get('selector'),
                                                        selector.get('selector_attribute')))
            return clean_data(elems=elems, selector=selector)
