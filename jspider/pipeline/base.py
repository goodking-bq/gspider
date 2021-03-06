# coding:utf-8
from __future__ import absolute_import, unicode_literals
import asyncio
from logging import getLogger

__author__ = "golden"
__date__ = '2018/5/29'


class BasePipeLine(object):
    def __init__(self, spider=None):
        self.has_done = False
        self.spider = spider
        self.logger = None
        self.set_logger()

    @classmethod
    def from_spider(cls, spider):
        pipe = cls(spider)
        return pipe

    async def process_item(self, item):
        self.logger.info(item)

    async def start(self):
        self.logger.debug('PipeLine starting ...')
        while await self.spider.doing() or not self.spider.downloader.has_done:
            self.logger.debug('download %s' % self.spider.downloader.has_done)
            item = await self.spider.item_queue.pop()
            if not item:
                await asyncio.sleep(1)
            else:
                await self.process_item(item)
        self.logger.info('PipeLine stop')
        self.has_done = True

    def set_logger(self):
        self.logger = getLogger(self.__class__.__name__)
        self.logger.debug("{name} setup success.".format(name=self.__class__.__name__))
