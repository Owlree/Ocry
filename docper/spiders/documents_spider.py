from typing import List, Callable

import scrapy


"""Takes links to all pdf files and sends them through the pipeline.
"""
class DocumentsSpider(scrapy.spiders.CrawlSpider):
    name: str = "documents"
    allowed_domains: List[str] = ["ms.ro"]
    start_urls: List[str] = ["http://www.ms.ro/"]
    rules: List[scrapy.spiders.Rule] = [
        scrapy.spiders.Rule(
            scrapy.linkextractors.LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_docs",
            process_request="process_request"
        )
    ]

    """Parses a scrapy response and saves links to all pdf files found
    """
    def parse_docs(self, response: scrapy.http.Response):
        pdfs: List[str] = []
        for url in response.css('a::attr(href)'):
            full = response.urljoin(url.extract())
            if full.endswith('.pdf'):
                pdfs.append(full)
        yield {
            'from': response.url,
            'file_urls': pdfs
        }

    """Filter requests we don't want.
    """
    def process_request(self, request: scrapy.http.Request):

        # Every rules should be pushed in this list
        rules: List[Callable[scrapy.http.Request], bool] = []

        def no_subdomains(request: scrapy.http.Request) -> bool:
            url: str = request.url
            for domain in self.allowed_domains:
                if '.' + domain in url and 'www.' + domain not in url:
                    return False
            return True
        rules.append((no_subdomains, 'No subdomains allowed'))

        # Evaluate rules
        for rule, message in rules:
            if not rule(request):
                self.logger.debug('Filtering %s: %s', request.url, message)
                return None

        return request
