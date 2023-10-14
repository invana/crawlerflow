
def test_string_extractor(html_extractor):
    result = html_extractor.extract()
    assert type(result) is dict
    assert result['title'] ==  'Hello, Parsel!'

def test_image_extractor(html_extractor):
    result = html_extractor.extract()
    assert type(result) is dict
    assert result['cover_pic'] ==  'https://placehold.co/600x400.png'

def test_list_of_dict_extractor(html_extractor):
    result = html_extractor.extract()
    assert type(result) is dict
    assert type(result['header_links']) is list
    assert len(result['header_links']) == 2
    assert result['header_links'][0]['link'] == 'http://example.com'

def test_href_extractor(html_extractor):
    result = html_extractor.extract()
    assert result['header_links'][0]['link'] == 'http://example.com'

