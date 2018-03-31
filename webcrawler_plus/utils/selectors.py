

def get_selector_element(html_element, selector, ):
    if selector.get('selector_attribute') in ['text']:
        if selector.get('selector_type') == 'css':
            elems = html_element.css("{0}::{1}".format(selector.get('selector'),
                                                       selector.get('selector_attribute')))
            return elems if selector.get('multiple') else elems.extract_first()
        else:
            raise NotImplemented("selector_type not equal to css; this is not implemented")
    elif selector.get('selector_attribute') == 'html':
        if selector.get('selector_type') == 'css':
            elems = html_element.css(selector.get('selector'))
            return elems if selector.get('multiple') else elems.extract_first()
        else:
            raise NotImplemented("selector_type not equal to css; this is not implemented")
    else:
        if selector.get('selector_type') == 'css':
            elems = html_element.css(selector.get('selector')) \
                .xpath("@{0}".format(selector.get('selector_attribute')))
            return elems if selector.get('multiple') else elems.extract_first()
        else:
            raise NotImplemented("selector_type not equal to css; this is not implemented")

