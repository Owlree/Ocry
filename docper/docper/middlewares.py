"""All middlewares for docper are described and implemented in this module.
"""


import scrapy


"""Enhances the requests with a depth property to allow DEPTH_LIMIT setting to
work with spiders that inherit from CrawlSpider.

This comes as a workaround to the fact that CrawlSpider does not propagate 
depth poperly.
"""
class StickyDepthSpiderMiddleware:

    """Takes the depth property from the response and adds it to all outgoing
    requests.
    """
    def process_spider_output(self, response, result, spider):
        for x in result:
            if isinstance(x, scrapy.http.Request):
                x.meta.setdefault('depth', response.meta.get('depth', 0))
                
            # We must yield all requests and responses, we don't filter 
            # anything here
            yield x
