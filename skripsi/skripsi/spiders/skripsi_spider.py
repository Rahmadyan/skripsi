import scrapy
import datetime
from ..items import SkripsiItem
# import sys
# sys.path.insert(0, '../metode/tanggalan')
from ..spiders.tanggalan import convert

# from test import lakukan_perhitungan
#
# from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher

class SkripsiSpiderSpider(scrapy.Spider):
    name = 'skripsi'
    # custom_settings = {'CLOSESPIDER_ITEMCOUNT': 10}
    start_urls = ['https://nasional.sindonews.com/topic/9695/pemilu-2019/']

    # def __init__(self):
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):

        for href in response.css('.lnk-t a::attr(href)'):
            yield response.follow(href, self.parse_author)

        # for href in response.css('.newpaging li:nth-child(4) a::attr(href)'):
        #     yield response.follow(href, self.parse)

    def parse_author(self, response):

        items = SkripsiItem()
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        content = response.xpath(".//div[@class='vidy-embed']/descendant::text()").extract()
        x = response.css('time::text').extract()
        a = convert(x)
        items['url'] = response.url,
        items['title'] = extract_with_css('h1::text'),
        items['author'] = extract_with_css('.author a::text'),
        # items['time'] = extract_with_css('time::text'),
        items['time'] = a,
        items['crawl_time'] = datetime.datetime.now(),
        items['imagelink'] = extract_with_css('.article img::attr(src)'),
        items['content'] = ''.join(content),

        yield items

    # def spider_closed(self, spider):
    #     lakukan_perhitungan()