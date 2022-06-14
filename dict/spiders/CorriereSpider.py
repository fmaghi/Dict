import string

import scrapy
from scrapy import Selector

BROWSE_URL = 'https://dizionari.corriere.it/dizionario_italiano/'
DICT_URL = 'https://dizionari.corriere.it/dizionario_italiano/'
TEST_URL = 'https://dizionari.corriere.it/dizionario_italiano/a.shtml'
PAGE_SUFFIX = '.shtml'
URL_FILE = 'corriere/urls'
FAILED_LOG = 'corriere/failed'

class CorriereSpider(scrapy.Spider):
    name = "corriere"

    def start_requests(self):
        # # test
        # yield scrapy.Request(url=TEST_URL, callback=self.test)
        for letter in string.ascii_lowercase:
            letter_url = BROWSE_URL + letter + PAGE_SUFFIX
            # get page number
            yield scrapy.Request(url=letter_url, meta={'letter': letter, 'page': 1}, callback=self.get_page_range)

    def get_page_range(self, response):
        if response.status == 404:
            with open(FAILED_LOG, 'a') as f:
                f.write('404: ' + response.url + '\n')
        else:
            sel = Selector(response)
    
            wordlist = sel.xpath("//div[@class='diz-chapterListBig']/a/@href").extract()
            if len(wordlist):
                with open(URL_FILE, 'a') as f:
                    for word in wordlist:
                        url = BROWSE_URL + word + '\n'
                        f.write(url)
    
                letter = response.meta.get('letter')
                page_number = response.meta.get('page') + 1
                next_page = f'{BROWSE_URL}{letter}_{page_number}.shtml'
                # keeps requesting until nothing is in the page
                yield scrapy.Request(url=next_page, meta={'letter': letter, 'page': page_number}, callback=self.get_page_range)
            else:
                with open(FAILED_LOG, 'a') as f:
                    f.write('empty: ' + response.url + '\n')

    def test(self, response):
        sel = Selector(response)

        wordlist = sel.xpath("//div[@class='diz-chapterListBig']/a/@href").extract()
        with open(URL_FILE, 'w') as f:
            if len(wordlist):
                urls = []
                for word in wordlist:
                    urls.append(BROWSE_URL + word + '\n')

                f.writelines(urls)
            else:
                f.write('nothing found!')

