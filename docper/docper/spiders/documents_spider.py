import scrapy

from typing import List

class DocumentsSpider(scrapy.spiders.CrawlSpider):
    name: str = "documents"
    allowed_domains = ["ms.ro"]
    start_urls = ["http://www.ms.ro/"]
    rules = [
        scrapy.spiders.Rule(
            scrapy.linkextractors.LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_docs"
        )
    ]

    """ Parses a scrapy response and saves links to all pdf files found
    """
    def parse_docs(self, response: scrapy.http.Response):
        for url in response.css('a::attr(href)'):
            full = response.urljoin(url.extract())
            if full.endswith('.pdf'):
                yield {
                    'document': full,
                    'from': response.url
                }
