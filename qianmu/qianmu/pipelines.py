# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
import pymysql
import logging
import redis

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CheckPipeline(object):
    def process_item(self, item, spider):
        if not item['undergraduate_num'] or not item['postgraduate_num']:
            raise DropItem('Misssing field in %s' % item)
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = None
        self.cur = None

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='rock1204',
            db='university',
            charset='utf8',
        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        # cols, values = zip(*[(col, item[col]) for col in item.keys()])
        cols, values = zip(*item.items())

        cols = ['%s' % key for key in cols]
        sql = "INSERT INTO `universities`(%s) VALUES (%s);" % (','.join(cols), ','.join(['%s'] * len(cols)))
        # 防止sql注入: execute方法会将特殊字符转义,如果字符中具有sql语句会被注入
        # 将values列表作为参数传入可以防止被转义
        self.cur.execute(sql, values)
        print(sql)
        print(values)
        self.conn.commit()
        logger.info(self.cur._last_executed)
        return item


class RedisPipeline(object):
    def __init__(self):
        self.redis = redis.Redis(db=10)

    def process_item(self, item, spider):
        self.redis.sadd(spider.name, item['name'])
        logger.info('redis: add %s to %s' % (item['name'], spider.name))
        return item
