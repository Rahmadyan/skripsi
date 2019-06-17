import scrapy
from ..items import SkripsiItem

class SkripsiSpider3(scrapy.Spider):
    name = 'skripsi3'
    page_number = 2
    start_urls = ['https://tirto.id/q/politik-bpt']

    def parse(self, response):
        for href in response.css('a::attr(href)'):
            yield response.follow(href, self.parse_author)

        previous_page = 'https://tirto.id/q/politik-bpt/'+ str(SkripsiSpider3.page_number) +''
        if SkripsiSpider3.page_number <=3:
            SkripsiSpider3.page_number += 1
            yield response.follow(previous_page, callback = self.parse)
        # for href in response.css('.pagination-sm a::attr(href)'):
        #     yield response.follow(href, self.parse)

    def parse_author(self, response):

        items = SkripsiItem()
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        content = response.xpath(".//div[@class='content-text-editor']/descendant::text()").extract()
        items['title'] = extract_with_css('.my-3::text'),
        items['time'] = extract_with_css('.text-left::text'),
        items['imagelink'] = extract_with_css('a img::attr(src)'),
        items['content'] = ''.join(content),

        yield items