import scrapy
import datetime
from ..items import SkripsiItem

class SkripsiSpider3(scrapy.Spider):
    name = 'skripsi4'
    page_number = 2
    custom_settings = {'CLOSESPIDER_ITEMCOUNT': 10}
    start_urls = ['https://www.detik.com/pemilu']

    def parse(self, response):
        link = response.css("li article a").xpath("@href").extract()
        for href in link:
            yield response.follow(href, self.parse_author)

        previous_page = 'https://www.detik.com/pemilu/'+ str(SkripsiSpider3.page_number) +''
        if SkripsiSpider3.page_number <=3:
            SkripsiSpider3.page_number += 1
            yield response.follow(previous_page, callback = self.parse)


    def parse_author(self, response):
        items = SkripsiItem()
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        content = response.xpath(".//div[@class='itp_bodycontent detail_text']/text()").extract()
        # time = response.css("jdl .date::text").extract()
        items['url'] = response.url,
        items['title']= extract_with_css('h1::text'),
        items['author'] = extract_with_css('.author::text'),
        items['time']= extract_with_css('.jdl .date::text'),
        # items['time']=time,
        items['crawl_time'] = datetime.datetime.now(),
        items['imagelink']= extract_with_css('.pic_artikel img::attr(src)'),
        if response.xpath(".//div[@class='itp_bodycontent detail_text']/text()"):
            items['content']= ''.join(content),
        yield items


