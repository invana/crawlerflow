"""
change this logic according to your requirements.

You can access the parser data using context['parser_1']
"""


def transformation_fn(context):
    cleaned_data = []
    for res in context:
        print("res>>>>>", res)
        item = res.get("extracted_data", {}).get("page-seo-data", None)
        print("item<>>>><<<<<>>>>", item)
        item_context = res.get("context", {})
        if item:
            item['url'] = res['url']
            item['context'] = item_context
            if "wikipedia" in res['url']:
                cleaned_data.append(item)
    return cleaned_data
