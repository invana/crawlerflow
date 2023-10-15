def transformation_fn(context):
    cleaned_data = []
    for res in context:
        item = res.get("page-seo-data", None)
        item_context = res.get("context", {})
        if item:
            item['url'] = res['url']
            item['context'] = item_context
            cleaned_data.append(item)
    return cleaned_data
