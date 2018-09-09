# coding=utf-8
import logging
from abc import ABCMeta, abstractmethod, abstractproperty

from db.third_post_db import third_post_db
from conf.logger import log


# 爬虫基类
class Crawler:
    __metaclass__ = ABCMeta

    third_id = None  # 第三方平台id
    third_name = None  # 第三方平台名称

    def __init__(self):
        pass

    @abstractmethod
    def _craw(self, url, param=None, *args):
        pass

    @abstractmethod
    def start(self):
        pass

    # 批量插入
    def batch_insert(self, res_list):
        if len(res_list) > 0:
            r_list = []
            for l in res_list:
                item = (l.third_id, l.third_name, l.post_id, l.title, l.tags, l.author, l.content,
                        l.like_num, l.comment_num, l.redirect_url, l.creatime, l.can_analysis)
                r_list.append(item)
            # 批量入库
            log.info("执行db操作,%s文章入库", self.third_name)
            third_post_db.batch_insert(r_list)
