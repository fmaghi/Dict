# scrapy crawl url -a path=/path/with/url/list
import os.path
import scrapy


class UrlSpider(scrapy.Spider):
    name = "url"

    def __init__(self, path=None, *args, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.failed = []

    def start_requests(self):
        url_path = self.path + '/urls'
        html_path = self.path + '/html'

        if not os.path.exists(html_path):
            os.makedirs(html_path)

        with open(url_path, 'r') as file:
            urls = file.readlines()
            for url in urls:
                yield scrapy.Request(url=url, meta={'html_path': html_path}, callback=self.parse)

        with open(f'{self.path}/failed.log', 'w') as log:
            log.writelines(self.failed)

    def parse(self, response):
        page = response.url.split("/")[-1]
        path = response.meta.get('html_path')

        filename = f'{path}/{page}.html'

        with open(filename, 'wb') as f:
            f.write(response.body)

