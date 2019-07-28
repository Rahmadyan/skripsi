# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
# import sys
# sys.path.insert(0, '../metode')
# from test import lakukan_perhitungan

# from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher

class SkripsiPipeline(object):

    def __init__(self):
        self.create_connection()
        # dispatcher.connect(self.close_spider, signals.close_spider)
        # self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = '127.0.0.1',
            password = '',
            user = 'root',
            database = 'news'
        )
        self.curr = self.conn.cursor()

    # def create_table(self):
    #     self.curr.execute("""DROP TABLE IF EXISTS news_tb""")
    #     self.curr.execute("""CREATE TABLE news_tb(
    #                         id INT NOT NULL AUTO_INCREMENT,
    #                         title text,
    #                         time text,
    #                         imagelink text,
    #                         content varchar 10000
    #                         PRIMARY KEY (id)
    #                         )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self,item):
        self.curr.execute("INSERT INTO news_tb (url, title, author, time, crawl_time, imagelink, content) values (%s,%s,%s,%s,%s,%s,%s)",(
            item['url'][0],
            item['title'][0],
            item['author'][0],
            item['time'][0],
            item['crawl_time'][0],
            item['imagelink'][0],
            item['content'][0]
        ))
        self.conn.commit()
    #
    # def close_spider(self, spider):
    #     lakukan_perhitungan()


