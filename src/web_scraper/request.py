

class CrawlRequest:

    def __init__(self, url, referrer=None, **meta) -> None:
        self.url: str = url
        self.meta: dict = meta

    def __str__(self) -> str:
        return f"<CrawlRequest: {self.url}>"