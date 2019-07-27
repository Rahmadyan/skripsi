import scrapy
from ..items import SkripsiItem

class SkripsiSpiderSpider(scrapy.Spider):
    name = 'skripsi2'
    custom_settings = {'CLOSESPIDER_ITEMCOUNT': 10}
    start_urls = ['https://www.tribunnews.com/topic/pemilu-2019']

    def parse(self, response):

        for href in response.css('h3.f20 a::attr(href)'):
            yield response.follow(href, self.parse_author)

        for href in response.css('a:nth-child(5)::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_author(self, response):

        items = SkripsiItem()
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        content = response.xpath(".//div[@class='side-article txt-article']/p/text()").extract()
        items['url'] = response.url,
        items['title'] = extract_with_css('#arttitle::text'),
        items['author'] = extract_with_css('#penulis::text'),
        items['time'] = extract_with_css('time.grey::text'),
        items['imagelink'] = extract_with_css('div.imgfull_div img::attr(src)'),
        items['content'] = ''.join(content),

        yield items



# import scrapy
# from ..items import SkripsiItem
#
# class SkripsiSpiderSpider(scrapy.Spider):
#     name = 'skripsi2'
#     page_number = 2
#     start_urls = ['https://www.antaranews.com/politik/3']
#
#     def parse(self, response):
#
#         for href in response.css('.simple-big h3 a::attr(href)'):
#             yield response.follow(href, self.parse_author)
#
#         previous_page = 'https://www.detik.com/pemilu/'+ str(SkripsiSpiderSpider.page_number) +''
#         if SkripsiSpiderSpider.page_number <=3:
#             SkripsiSpiderSpider.page_number += 1
#             yield response.follow(previous_page, callback = self.parse)
#         # for href in response.css('.pagination-sm a::attr(href)'):
#         #     yield response.follow(href, self.parse)
#
#     def parse_author(self, response):
#
#         items = SkripsiItem()
#         def extract_with_css(query):
#             return response.css(query).get(default='').strip()
#
#         content = response.xpath(".//div[@class='post-content clearfix']/descendant::text()").extract()
#
#         items['title'] = extract_with_css('.post-title::text'),
#         items['time'] = extract_with_css('.post-header .article-date::text'),
#         items['imagelink'] = extract_with_css('.post-header img::attr(src)'),
#         items['content'] = ''.join(content),
#
#         yield items