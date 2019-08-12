"""
change this logic according to your requirements.

You can access the parser data using context['parser_1']
"""


def transformation_fn(context):
    cleaned_data = []
    for res in context:
        item = res.get("extracted_data", {}).get("page-seo-data", None)
        if item:
            item['url'] = res['url']
            if "wikipedia" in res['url']:
                cleaned_data.append(item)
    return cleaned_data
