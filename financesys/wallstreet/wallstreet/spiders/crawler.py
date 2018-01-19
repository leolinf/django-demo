#!/usr/bin/env python
# encoding: utf-8
import datetime
from wallstreet.items import WallstreetItem
from scrapy import Spider
from scrapy import Request
from scrapy.selector import Selector


class WallCrawler(Spider):
    name = "wallstreet"
    allowed_domains = ["wallstreetcn.com"]
    start_urls = [
        "http://live.wallstreetcn.com/",
    ]

    def parse(self, response):
        '''爬取规则'''
        html = Selector(response)
        conts = html.xpath('//li[@class="news type-text"]')
        for cont in conts:
            item = WallstreetItem()
            item['date'] = cont.xpath('@data-day').extract()[0]
            item['time'] = cont.xpath('.//span[@class="time"]/text()').extract()[0]
            item['relationship'] = int(cont.xpath('@data-importance').extract()[0])
            detail_url = 'http://live.wallstreetcn.com' + cont.xpath('.//a/@href').extract()[0]
            item['url'] = detail_url
            # item['content']= cont.xpath('.//div[@class="content"]/p/text()').extract()[0]
            yield Request(detail_url, callback=self.parse_item, meta={'item': item})

    def parse_item(self, response):
        '''进一步爬取'''
        item = response.meta['item']
        parse_html = Selector(response)
        release_time = parse_html.xpath('//span[@class="item time"]/text()')\
            .extract()[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', '')
        release_times = datetime.datetime.strptime(release_time, "%Y-%m-%d %H:%M:%S")
        item['release_time'] = release_times
        item['title'] = parse_html.xpath('//h1[@class="article-title"]/text()').extract()[0]
        item['content'] = parse_html.xpath('//div[@class="article-content"]/p/text()').extract()
        item['page_view'] = int(parse_html.xpath('//strong[@id="js-read-times-text"]/text()').extract()[0])
        item['author'] = parse_html.xpath('//a[@class="item author"]/text()').extract()[0]
        yield item
