import json
import scrapy
import scrapy.pipelines.files
from urllib.parse import urlparse


# TODO(Owlree): Move this to settings maybe
_DOMAIN_NAMES = {
    'www.ms.ro': 'sanatate',
    'old.ms.ro': 'sanatate'
}


"""We defined this class because we want to save some metadata [...]
"""
class DocperFilesPipeline(scrapy.pipelines.files.FilesPipeline):
    
    """We override this because we want so save metadatata for all downloaded
    files.
    """
    def item_completed(self, results, item, info):
        files = [x for ok, x in results if ok]
        if not files:
            raise scrapy.exceptions.DropItem("Item contains no files")
        item['files'] = files
        del item['file_urls']
        return item
        
    """We override this because the 'full' directory was not very expressive,
    we want to replace it with something that is.
    """
    def file_path(self, request, response=None, info=None) -> str:
        path: str = super().file_path(request, response=response, info=info)
        netloc: str = urlparse(request.url).netloc
        domain_name = _DOMAIN_NAMES.get(netloc, netloc)
        return path.replace('full/', domain_name + '/')
