# Terminology


**crawlers** : single unit of CTI flow. A crawler has extractors, traversals.

**traversal**: definition of how one crawler will navigate to another one. 

**extractor** : Definition of what data to extract from the web page and how it should be saved in to 
the database. Extractor will have a definition of multiple selectors that should be extracted.

**selector** : Definition of a unit data that will be extracted by extractor.

**transformation** : Instructions that tells how to convert crawled data into a final data. This is the step 
where user can clean or convert the data into the desired formats.

**callbacks** : Callbacks that should be pinged once the job is done, so that other jobs can be triggered by integrations.

**context** : This data will added to each entry that is saved by the crawler. This data is something you might want
to carry forward to all the crawling jobs and saved entries. 

Example: `context = {"author" : "rrmerugu", "project_id": "alien-data"}` will save this in all the crawl extracted data.