BOT_NAME = 'docper'

SPIDER_MODULES = ['docper.spiders']
NEWSPIDER_MODULE = 'docper.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'docper.pipelines.DocperFilesPipeline': 1
}

SPIDER_MIDDLEWARES = {
    'docper.middlewares.StickyDepthSpiderMiddleware': 1
}

DEPTH_LIMIT = 1

RETRY_ENABLED = False
COOKIES_ENABLED = False
LOG_LEVEL = 'INFO'

DOWNLOAD_TIMEOUT = 20

## Uncomment these lines to enable AWS S3 upload
# FILES_STORE = 's3://bucker/folder/'
# AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
# AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7'
DOWNLOAD_DELAY = 0.25
