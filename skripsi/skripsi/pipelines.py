# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector

class SkripsiPipeline(object):

    def __init__(self):
        self.create_connection()
        # self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
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
        self.curr.execute("INSERT INTO news_tb (title, author, time, imagelink, content) values (%s,%s,%s,%s,%s)",(
            item['title'][0],
            item['author'][0],
            item['time'][0],
            item['imagelink'][0],
            item['content'][0]
        ))
        self.conn.commit()



