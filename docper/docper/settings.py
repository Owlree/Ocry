BOT_NAME = 'docper'

SPIDER_MODULES = ['docper.spiders']
NEWSPIDER_MODULE = 'docper.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'docper.pipelines.JsonWriterPipeline': 300,
}

SPIDER_MIDDLEWARES = { 'docper.middlewares.StickyDepthSpiderMiddleware' : 100 }

DEPTH_LIMIT = 5

RETRY_ENABLED = False
COOKIES_ENABLED = False
LOG_LEVEL = 'INFO'

DOWNLOAD_TIMEOUT = 20
