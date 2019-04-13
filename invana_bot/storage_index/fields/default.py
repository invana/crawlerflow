"""
This component need to be revisited. Inspired by the component built for invana internal crawlers.
Need to find a way to implement with the current architecture.


"""


class ElementBase(object):
    nth_element = 0
    value_type = None

    def __init__(self, data_attribute=None, nth_element=None, **kwargs):
        if nth_element is not None:
            self.nth_element = nth_element
        self.data_attribute = data_attribute

    def validate_data(self):
        pass


class LinkElement(ElementBase):
    value_type = "href"


class HTMLElement(ElementBase):
    value_type = "innerHTML"


class TextElement(ElementBase):
    value_type = "text"


class ImageElement(ElementBase):
    value_type = "src"


class ListElement(object):
    is_multiple = True

    def __init__(self, instance, **kwargs):
        a = instance()
        pass
