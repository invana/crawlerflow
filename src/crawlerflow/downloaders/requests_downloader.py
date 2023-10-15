from scrapy.http import HtmlResponse, Response, JsonRequest, TextResponse
import requests
from scrapy.downloadermiddlewares.httpcompression import ACCEPTED_ENCODINGS


class RequestsDownloaderMiddleware(object):

    def process_request(self, request, spider):
        if spider.settings.getbool("COMPRESSION_ENABLED"):
            request.headers.setdefault("Accept-Encoding", b", ".join(ACCEPTED_ENCODINGS))

    def process_request(self, request, spider):
        # only spiders with downloader = requests should trigger this.
        if not spider.downloader and spider.downloader != "requests":
            return
        headers = {x.decode(): request.headers[x].decode() for x in request.headers}
        kwargs = { "headers":headers, "cookies" :request.cookies}
        if spider.settings.getbool("COMPRESSION_ENABLED"):
            kwargs['stream'] = True
        res = requests.get(request.url, **kwargs)
        body=res.raw.read() if spider.settings.getbool("COMPRESSION_ENABLED") else res.content
        response = Response(request.url, 
                            body=body, 
                            headers=res.headers, 
                            status=res.status_code, 
                            request=request)
        return response