# Quick start



You can apply multiple transformations on the crawled data. Transformations are applied once 
all the spiders in the CTI flow are done.

Here is how you define a transformation. You need to add the transformation config in yaml . Each 
trasnformation would contain two things:

1. transformation_id : name of the transformation(sluggified version is the only right way now )
2. transformation_fn : name of the python function in the `cti_transformations.py`(for cti flow) or
 `crawler_transformations.py`(for single crawler)


```yaml
# cti_manifest.yml or crawler_manifest.yml

transformations:
- transformation_id: default
  transformation_fn: transformation_fn
  
- index_id: primary_db
  transformation_id: default
  connection_uri: mongodb://127.0.0.1/spiders_data_index
  collection_name: blog_list
  unique_key: url
```

```python
# cti_transformations.py or crawler_transformations.py

  
def transformation_fn(results):
    """
    results will contain all the documents that are stored in the database during a given cti/crawler job.
    if you want to identify the data of a parser data with in the results. You can use the example below.
    
    """
        
    results_cleaned = []
    for result in results:
        blog_list_parser_data = result.get("blog_list_parser",{})
        if blog_list_parser_data:
            for blog in blog_list_parser_data.get("blogs",[]):
                results_cleaned.append(blog)
                
    return results_cleaned



```