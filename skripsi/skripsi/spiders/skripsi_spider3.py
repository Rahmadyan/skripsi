import scrapy
from ..items import SkripsiItem

class SkripsiSpiderSpider(scrapy.Spider):
    name = 'skripsi3'
    page_number = 2
    start_urls = ['https://www.detik.com/pemilu/']

    def parse(self, response):

        for href in response.css('.sub_judul+ h2::attr(href)'):
            yield response.follow(href, self.parse_author)

        previous_page = 'https://www.detik.com/pemilu/'+ str(SkripsiSpiderSpider.page_number) +''
        if SkripsiSpiderSpider.page_number <=3:
            SkripsiSpiderSpider.page_number += 1
            yield response.follow(previous_page, callback = self.parse)
        # for href in response.css('.pagination-sm a::attr(href)'):
        #     yield response.follow(href, self.parse)

    def parse_author(self, response):

        items = SkripsiItem()
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        content = response.xpath(".//div[@class='itp_bodycontent detail_text']/descendant::text()").extract()

        items['title'] = extract_with_css('h1::text'),
        items['time'] = extract_with_css('.jdl .date::text'),
        items['imagelink'] = extract_with_css('.pic_artikel img::attr(src)'),
        items['content'] = ''.join(content),

        yield items