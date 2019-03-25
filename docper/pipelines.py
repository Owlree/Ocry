import json


class DocperPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(
            dict(item), 
            ensure_ascii=False, 
            sort_keys=True)
        self.file.write(line + '\n')
        return item
