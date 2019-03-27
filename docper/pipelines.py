import os
import json
import scrapy
import boto3
import scrapy.pipelines.files
from urllib.parse import urlparse, urljoin


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
            raise scrapy.exceptions.DropItem('Item contains no files')
        del item['file_urls']
        item['files'] = files
        item['downloaded'] = True
        return item

    """We override this because the 'full' directory was not very expressive,
    we want to replace it with something that is.
    """
    def file_path(self, request, response=None, info=None) -> str:
        path: str = super().file_path(request, response=response, info=info)
        netloc: str = urlparse(request.url).netloc
        domain_name = _DOMAIN_NAMES.get(netloc, netloc)
        return path.replace('full/', domain_name + '/')


class DynamoDBMetadata:
    def process_item(self, item, spider):
        if not item.get('downloaded', False):
            return item
        settings = scrapy.utils.project.get_project_settings()

        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=settings.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=settings.get('AWS_SECRET_ACCESS_KEY'),
            region_name=settings.get('AWS_REGION_NAME'))
        table = dynamodb.Table(settings.get('AWS_DYNAMODB_METADATA_TABLE'))
        s3path: str = settings.get('FILES_STORE').replace(
            '{}://'.format(urlparse(settings.get('FILES_STORE')).scheme), '')
        print(s3path)

        for f in item['files']:
            f['name'] = f['path'].split('/')[-1].replace('.pdf', '')
            f['path'] = urljoin(
                'https://s3-eu-west-1.amazonaws.com',
                os.path.join(s3path, f['path']))
            table.put_item(Item=f)
        return item
