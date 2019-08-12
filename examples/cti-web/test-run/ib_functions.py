"""
change this logic according to your requirements.

You can access the parser data using context['parser_1']
"""    
def transformation_fn(context):
    print("=======>>>> product review extractor <<<<========")
    cleaned_data = []
    for res in context:
        item = res.get("page-seo-data", None)
        item_context = res.get("context", {})
        if item:
            item['url'] = res['url']
            item['context'] = item_context
            cleaned_data.append(item)
    return cleaned_data

