import scrapy
import datetime
from ..items import SkripsiItem

class SkripsiSpiderSpider(scrapy.Spider):
    name = 'skripsi'
    # custom_settings = {'CLOSESPIDER_ITEMCOUNT': 10}
    start_urls = ['https://nasional.sindonews.com/topic/9695/pemilu-2019/']

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
        # time = response.css('time::text').extract()
        # time.strptime(' '.join(time.rsplit(' ', 4)[0:4]), "%A, %B %d, %Y")
        items['url'] = response.url,
        items['title'] = extract_with_css('h1::text'),
        items['author'] = extract_with_css('.author a::text'),
        items['time'] = extract_with_css('time::text'),
        items['crawl_time'] = datetime.datetime.now(),
        items['imagelink'] = extract_with_css('.article img::attr(src)'),
        items['content'] = ''.join(content),

        yield items