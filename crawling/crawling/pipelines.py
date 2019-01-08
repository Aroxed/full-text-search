# -*- coding: utf-8 -*-

import lxml.etree
import lxml.html
from html2text import HTML2Text


class CleaningHTMLPipeline(object):

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

    def process_item(self, item, spider):
        root = lxml.html.fromstring(item['body'])
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head", "style")
        txt = lxml.html.tostring(root, method="text", encoding='unicode')
        item['body'] = self.to_text(txt)
        return item


class IndexingPipeline(object):
    def process_item(self, item, spider):
        spider.indexer.add_document(item)
        return item
