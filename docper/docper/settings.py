BOT_NAME = 'docper'

SPIDER_MODULES = ['docper.spiders']
NEWSPIDER_MODULE = 'docper.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'scrapy.pipelines.files.FilesPipeline': 1
}

SPIDER_MIDDLEWARES = {
    'docper.middlewares.StickyDepthSpiderMiddleware' : 100
}

DEPTH_LIMIT = 5

RETRY_ENABLED = False
COOKIES_ENABLED = False
LOG_LEVEL = 'INFO'

DOWNLOAD_TIMEOUT = 20

## Uncomment these lines to enable AWS S3 upload
# FILES_STORE = 's3://bucker/folder/'
# AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
# AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
