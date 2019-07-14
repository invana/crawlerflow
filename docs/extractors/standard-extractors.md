# Standard Extractor


InvanaBot allows users to extract information while it crawls through the webpages. You can specify multiple
extractors to a crawler, allowing you to organise the information you need into grouped/subdocument data.


All the extractors are available at `invana_bot.extractors`



## ParagraphsExtractor

Here is the configuration.

```yaml
spiders:
- spider_id: default_crawler
  extractors:
  - extractor_type: ParagraphsExtractor
    extractor_id: paragraphs_data
```

Here is the data extracted. This will return all the paragraphs as list.

```json
{
  "paragraphs_data" :  [
      "Here is the first paragraph",
      "Here is the second paragraph"
    ]
  
}
```


## TableContentExtractor


Here is the configuration.

```yaml
spiders:
- spider_id: default_crawler
  extractors:
  - extractor_type: TableContentExtractor
    extractor_id: tables_data
```

Here is the data extracted. This will return all the tables as list.

```json
{  
   "tables_data":[  
      [ // table 1
         {  
            "Code":"IN",
            "Country":"India",
            "Last Checked":"1 second ago"
         }
      ],
      [ // table 2
        {
            "Code": "DEL",
            "State": "New Delhi"
        }
      ]
   ]
} 
```

## MetaTagExtractor

Here is the configuration. This will gather data of og, twitter and fb meta tags, pretty much any 
`meta` element.

```yaml
spiders:
- spider_id: default_crawler
  extractors:
  - extractor_type: MetaTagExtractor
    extractor_id: meta_tag_data
```

Here is the data extracted. This will return all the `<meta>` tags data as dictionary.

```json
{
  "meta_tag_data":{  
      "meta__viewport":"width=device-width,initial-scale=1,maximum-scale=1",
      "meta__referrer":"origin",
      "meta__description":"Here is the description of the site ",
      "title":"Example site | Homepage"
   }
}
```


## IconsExtractor

Here is the configuration.

```yaml
spiders:
- spider_id: default_crawler
  extractors:
  - extractor_type: IconsExtractor
    extractor_id: icon_data
```

Here is the data extracted. This will return all the `<meta>` tags data as dictionary.



```json
{
  "icon_data": {
      "32x32": "https://example.com/2018/10/fav-icon.png?w=32",
      "192x192": "https://example.com/2018/10/fav-icon.png?w=120"
    }
}
```

## JSONLDExtractor

Here is the configuration. 

```yaml
spiders:
- spider_id: default_crawler
  extractors:
  - extractor_type: JSONLDExtractor
    extractor_id: json_ld_data
```

Here is the data extracted. The returned data would be in list, as there can be multiple json+ld 
descriptions in a single page. 

```json

{
  "json_ld_data": [
    {
      "@context": "http://schema.org",
      "@type": "NewsArticle",
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "https://example.com/article/technology/science/space-age/"
      },
      "url": "https://example.com/article/technology/science/space-age/",
      "articleBody": "Lorem ipusum, here is the article body.",
      "articleSection": "technology",
      "keywords": "Chandrayaan-2, Chandrayaan-2 launch, Chandrayaan-2 launch monday, Chandrayaan-2 launch timing, Chandrayaan-2 isro launch date time, Chandrayaan-2 launch july 15, isro moon, isro Chandrayaan-2, Chandrayaan-2 moon",
      "headline": "Chandrayaan-2 to launch India into new space age",
      "description": "The Chandrayaan-2, a moon-lander and rover mission, is designed to go where no spacecraft has gone before.",
      "datePublished": "2019-07-14T09:29:56+05:30",
      "dateModified": "2019-07-14T09:29:56+05:30",
      "publisher": {
        "@type": "Organization",
        "name": "MoonNews Publications",
        "logo": {
          "@type": "ImageObject",
          "url": "https://s2.wp.com/wp-content/themes/vip/example.com-v2/dist/images/ienewlogo3_new.png",
          "width": "600",
          "height": "60"
        }
      },
      "author": {
        "@type": "Person",
        "name": "John Doe",
        "sameAs": "https://example.com/profile/author/john-doe/"
      },
      "image": {
        "@type": "ImageObject",
        "url": "https://images.example.com/2019/07/chandrayaan-2_759-1.jpg",
        "width": "759",
        "height": "422"
      }
    },
    {
      "@context": "http://schema.org",
      "@type": "Person",
      "name": "John Doe",
      "url": "https://example.com/profile/author/john-doe/",
      "worksFor": {
        "@type": "Organization",
        "name": "MoonNews Publications",
        "url": "https://example.com/"
      }
    },
    {
      "@context": "http://schema.org",
      "@type": "WebSite",
      "url": "https://example.com/",
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://example.com/?s={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    }
  ]
}
```

## PlainHTMLContentExtractor

Here is the configuration. 

```yaml
spiders:
- spider_id: default_crawler
  extractors:
  - extractor_type: PlainHTMLContentExtractor
    extractor_id: html_content
```

Here is the data extracted. 

```json
{
  "html_content": "<html></body>Hello World!</body></html>"
}

```



## PageOverviewExtractor

Here is the configuration. 

```yaml
spiders:
- spider_id: default_crawler
  extractors:
  - extractor_type: PageOverviewExtractor
    extractor_id: overview
```

Here is the data extracted. 

```json


{  
   "overview":{  
      "title":"Welcome to the site.",
      "description":"Our space mission is designed to go where no spacecraft has gone before.",
      "image":"https://example.com/2019/07/image.jpg?w=759",
      "url":"https://example.com/article/technology/science/space-age/",
      "page_type":"article",
      "keywords":"space launch, chandrayaan-2 launch",
      "domain":"example.com",
      "first_paragraph":"First Paragraph comes here.",
      "shortlink_url":"https://example.com/?page=ok-me",
      "canonical_url":"https://example.com/article/technology/science/space-age/"
   }
}
```

## FeedUrlExtractor

Here is the configuration. 

```yaml
spiders:
- spider_id: default_crawler
  extractors:
  - extractor_type: FeedUrlExtractor
    extractor_id: feeds_data
```

Here is the data extracted. 

```json
{
  "feeds_data": {"rss__xml": "https://blog.scrapinghub.com/rss.xml", "rss__atom": null}
}

```
## ImagesExtractor


Here is the configuration. 

```yaml
spiders:
- spider_id: default_crawler
  extractors:
  - extractor_type: ImagesExtractor
    extractor_id: images
```

Here is the data extracted. 

```json
{
  "images": [
    "https://example.com/image-1.png",
    "https://example.com/image-2.png",
    "https://example.com/image-3.png"
  ]
}

```


## AllLinksExtractor

Here is the configuration. 

```yaml
spiders:
- spider_id: default_crawler
  extractors:
  - extractor_type: AllLinksExtractor
    extractor_id: all_links
```

Here is the data extracted. This will contains all links 

```json
{
  "all_links": [
    "https://example.com/page-1",
    "https://example.com/page-2",
    "https://example.com/page-3",
    "https://facebook.com/page-3",
    "https://twitter.com/page-3"
  ]
}

```



## AllLinksAnalyticsExtractor


Here is the configuration. 

```yaml
spiders:
- spider_id: default_crawler
  extractors:
  - extractor_type: AllLinksAnalyticsExtractor
    extractor_id: all_links_analysed
```

Here is the data extracted. This will contains all links in the page, seperating them into 
domain specific links.


```json
{  
   "links":[  
      {  
         "domain":"blog.scrapinghub.com",
         "links":[  
            "https://blog.scrapinghub.com",
            "https://blog.scrapinghub.com/web-data-analysis-exposing-nfl-player-salaries-with-python",
            "https://blog.scrapinghub.com/author/attila-tóth",
            "https://blog.scrapinghub.com/web-data-analysis-exposing-nfl-player-salaries-with-python#comments-listing",
            "https://blog.scrapinghub.com/spidermon-scrapy-spider-monitoring",
            "...",
            "https://blog.scrapinghub.com/alternative-financial-data-quality"
         ],
         "links_count":48
      },
      {  
         "domain":"overthecap.com",
         "links":[  
            "https://overthecap.com/",
            "https://overthecap.com/position/quarterback/"
         ],
         "links_count":2
      },
      {  
         "domain":"github.com",
         "links":[  
            "https://github.com/zseta/NFL-Contracts",
            "https://github.com/zseta/NFL-Contracts",
            "https://github.com/zseta/NFL-Contracts"
         ],
         "links_count":3
      },
      {  
         "domain":"scrapingauthority.com",
         "links":[  
            "https://scrapingauthority.com/resources/"
         ],
         "links_count":1
      },
      {  
         "domain":"twitter.com",
         "links":[  
            "https://twitter.com/share",
            "https://twitter.com/ScrapingHub"
         ],
         "links_count":2
      }

   ]

}
```