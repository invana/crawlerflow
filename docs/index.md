# InvanaBot Documentation


InvanaBot operates on **Crawl => Transform => Index** workflow. 


### About manifest.json:
- **cti_id** : unique identifier used to  
- **init_data** : json config that tells, from where the crawling should start.
    - **start_urls** 
- **crawlers** : a list of json based configurations that tells how to **traverse** and **parse** 
    - **parsers** : list of json configurations that tells crawler what data should be extracted from a web page.
    - **traversals** : list of json configurations that defines the pagination or which 
    page to goto.
- **transformations** : a list of python functions that can take `results` of current job as 
input and returns `cleaned_results` as output.
- **indexes** : a list of  that tells to what data storage, `cleaned_results` from different transformations 
 should be saved to 


Example of a 
