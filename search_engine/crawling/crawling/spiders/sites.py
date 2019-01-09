# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import pandas as pd
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from search_engine.crawling.crawling.items import CrawlingItem
from search_engine.indexing import Indexer


class SitesSpider(CrawlSpider):
    name = 'sites'

    def __init__(self, *args, **kwargs):
        super(SitesSpider, self).__init__(*args, **kwargs)
        df1 = pd.read_csv("Inc5000List_2017.csv", header=0, usecols=['website'])
        urls = [str(url) for url in list(df1['website'])]
        self.start_urls = urls
        self.allowed_domains = [str(urlparse(str(url)).netloc) for url in urls]

        self.indexer = Indexer()

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = CrawlingItem()
        item['title'] = response.xpath('//title/text()').extract()
        item['body'] = response.body
        item['url'] = response.request.url
        yield item
