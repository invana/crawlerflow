from parsel import Selector


class ExtractorBase:

    DATA_TYPES = {
        "StringField": str,
        "IntField": int,
        "FloatField": float,
        "DictField": dict
    }
    
    DEFAULT_DATA_TYPE = "StringField"

    def __init__(self, html,  extractor_fields):
        """
        :param html: html html of the request
        :param extractor_fields: extractor configuration in json; this is optional in most cases.
        """
        self.html = html if isinstance(html, Selector) else Selector(text=html)
        self.extractor_fields = extractor_fields or {}


    def get_elem_by_css(self, html_element, selector_string ):
        return html_element.css(selector_string)
 
    def get_value_by_css(self, html_element, selector_string, fetch_multiple_values=False):
        try:
            el = self.get_elem_by_css(html_element, selector_string )
            # el = el.xpath(f"@{attribute}") if attribute else  el  
            return el.get() if fetch_multiple_values is False else el.getall()
        except Exception as e:
            return None
    def get_data_type(self, type_string_raw):
        # type_string ;
        # examples usages: StringField; for list of StringField: [StringField]
        is_multiple = True if type(type_string_raw) is list else False
        type_string = type_string_raw[0] if is_multiple is True else type_string_raw
        return type_string, is_multiple

    def convert_to_data_type(self, data, type_string=None, is_multiple=True):
        data_type_cls = self.DATA_TYPES[type_string]
        if type_string in ["IntField", "FloatField"]:
            data = data.replace(',','')
        if data:          
            return data_type_cls(data) if is_multiple is False else [ data_type_cls(d) for d in data]
        return

    def extract_from_single_element(self, fields, html_element=None):
        data = {}
        html = html_element if html_element else self.html
        for field_name, field_config in fields.items():
            type_string, is_multiple = self.get_data_type(field_config.get('type', self.DEFAULT_DATA_TYPE)) 
            if type_string == "DictField":                   
                nested_fields =  field_config.get("fields", {})
                child_html_element = self.get_elem_by_css(html, field_config['selector'])                
                data[field_name] = self.extract_from_multiple_element(nested_fields, child_html_element) if is_multiple is True \
                            else  self.extract_from_single_element(nested_fields, html_element=child_html_element)
            else:
                extracted_data = self.get_value_by_css(html, field_config['selector'], fetch_multiple_values=is_multiple)
                data[field_name] = self.convert_to_data_type(extracted_data, type_string=type_string, is_multiple=is_multiple)
        return data
    
    def extract_from_multiple_element(self, fields, html_elements):
        data = []
        for html_element in html_elements:
            datum = self.extract_from_single_element(fields, html_element=html_element)
            data.append(datum)
        return data

    
    def extract_fields(self, fields:dict, html_element=None):
        return self.extract_from_single_element(fields, html_element=html_element)

 