import scrapy
from ..items import SkripsiItem

class SkripsiSpiderSpider(scrapy.Spider):
    name = 'skripsi'
    start_urls = ['https://nasional.sindonews.com/topic/9695/pemilu-2019/26']

    def parse(self, response):

        for href in response.css('.lnk-t a::attr(href)'):
            yield response.follow(href, self.parse_author)

        for href in response.css('.newpaging li:nth-child(1) a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_author(self, response):

        items = SkripsiItem()
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        content = response.xpath(".//div[@class='vidy-embed']/descendant::text()").extract()

        items['title'] = extract_with_css('h1::text'),
        items['author'] = extract_with_css('.author a::text'),
        items['time'] = extract_with_css('time::text'),
        items['imagelink'] = extract_with_css('.article img::attr(src)'),
        items['content'] = ''.join(content),

        yield items