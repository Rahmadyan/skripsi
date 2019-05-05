import scrapy
from ..items import SkripsiItem

class SkripsiSpiderSpider(scrapy.Spider):
    name = 'skripsi2'
    start_urls = ['https://www.antaranews.com/politik/3']

    def parse(self, response):

        for href in response.css('.simple-big h3 a::attr(href)'):
            yield response.follow(href, self.parse_author)

        for href in response.css('.pagination-sm a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_author(self, response):

        items = SkripsiItem()
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        content = response.xpath(".//div[@class='.entry-content']/descendant::text()").extract()

        items['title'] = extract_with_css('.post-title::text'),
        items['time'] = extract_with_css('.post-header .article-date::text'),
        items['imagelink'] = extract_with_css('.post-header img::attr(src)'),
        items['content'] = ''.join(content),

        yield items