# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pandas as pd
from scrapy.utils.markup import remove_tags
from urllib.parse import urlparse
import lxml.etree
import lxml.html
from html2text import HTML2Text

class SitesSpider(CrawlSpider):
    name = 'sites'

    def __init__(self, *args, **kwargs):
        super(SitesSpider, self).__init__(*args, **kwargs)
        df1 = pd.read_csv("companies.csv", header=0, usecols=['name', 'homepage_url', 'category_list', 'country_code'])
        urls = [str(url) for url in list(df1[900:1000]['homepage_url'])]
        self.start_urls = urls
        self.allowed_domains = [str(urlparse(str(url)).netloc) for url in urls]

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def to_text(self, html, rehtml=False):
        parser = HTML2Text()
        parser.wrap_links = False
        parser.skip_internal_links = True
        parser.inline_links = True
        parser.ignore_anchors = True
        parser.ignore_images = True
        parser.ignore_emphasis = True
        parser.ignore_links = True
        text = parser.handle(html)
        text = text.strip(' \t\n\r')
        if rehtml:
            text = text.replace('\n', '<br/>')
            text = text.replace('\\', '')
        return text

    def parse_item(self, response):

        #i['title'] = response.xpath('//title/text()').extract()
        root = lxml.html.fromstring(response.body)
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head", "style")
        txt = lxml.html.tostring(root, method="text", encoding='unicode')
        txt = self.to_text(txt)
        filename = 'collected/' + response.url.replace('/', '.').replace(':', '.') + '.txt'
        with open(filename, 'w') as f:
            f.write(txt)
