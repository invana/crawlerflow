


class ExtractorBase:

    DATA_TYPES = {
        "StringField": str,
        "IntField": int,
        "FloatField": float,
        "DictField": dict
    }
    DEFAULT_DATA_TYPE = "StringField"

    def __init__(self, html,  extractor_fields, extractor_fn=None):
        """
        :param html: html html of the request
        :param extractor_fields: extractor configuration in json; this is optional in most cases.
        :param extractor_fn: extractor python lambda; this is optional in most cases.
        """
        self.html = html
        self.extractor_fields = extractor_fields or {}
        self.extractor_fn = extractor_fn

    def get_elem_by_css(self, html_element, selector_string, attribute=None):
        # if attribute:
        # el =  
        return html_element.css(selector_string).xpath(f"@{attribute}") if attribute \
            else html_element.css(f"{selector_string}").xpath("/text()")
            # else html_element.css(f"{selector_string}::text") #el.xpath("/text()")
      
    def get_value_by_css(self, html_element, selector_string, attribute=None, fetch_multiple_values=False):
        el = self.get_elem_by_css(html_element, selector_string, attribute=attribute)
        # if attribute:
        #     el = el.xpath(f"@{attribute}")
        return el.get() if fetch_multiple_values is False else el.getall()
    

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
                extracted_data = self.get_value_by_css(html, field_config['selector'], attribute=field_config.get("attribute"), fetch_multiple_values=is_multiple)
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

 