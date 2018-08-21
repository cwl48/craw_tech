# -*- coding: utf-8 -*-
import requests
import arrow

from base.crawler import Crawler
from base.third_post import ThirdPost
from db.third_post_db import third_post_db
from conf.logger import log


# 2018-05-14 创建
# 掘金字段 d.entrylist
# objectId   唯一键值判断
# title 标题
# content 简述内容
# originalUrl  文章地址  跳转地址
# collectionCount 喜欢数量
# commentsCount 评论数
# createdAt 创建时间
# tags 标签 [] title标签名

class JueJin(Crawler):

    def __init__(self):
        super().__init__()
        self.third_id = 1
        self.third_name = "掘金"

    def _craw(self, url, param=None, *args):
        res = requests.get(url, params=param)
        if res.status_code == 200:
            like_total = args[0]  # 至少喜欢的数量
            # juejin response
            body_json = res.json()
            if body_json['s'] != 1:
                log.error("爬取掘金失败"+body_json['m'])
                return
            article_list = body_json['d']['entrylist']

            res_list = []
            for arti in article_list:

                data = third_post_db.find_by_pt_id(
                    arti['objectId'], self.third_id)

                if data is None and arti['collectionCount'] > like_total:  # 大于30喜欢的加入
                    # 构建
                    post = ThirdPost(self.third_id, self.third_name)
                    tags = []
                    for t in arti['tags']:
                        tags.append(t['title'])
                    post.tags = ",".join(tags)
                    # 顺序 文章id、标题、标签、作者、喜欢数、评论数、跳转url、创建时间
                    post.post_id = arti['objectId']
                    post.title = arti['title']
                    post.author = arti['user']['username']
                    post.content = arti['content']
                    post.like_num = arti['collectionCount']
                    post.comment_num = arti['commentsCount']
                    post.redirect_url = arti['originalUrl']
                    post.creatime = arrow.get(
                        arti['createdAt']).format('YYYY-MM-DD HH:mm:ss')

                    res_list.append(post)
            log.info("[%s]爬取-> %s  %d条记录", self.third_name, url, len(res_list))
            self.batch_insert(res_list)

    def start(self):
        # 资源
        src = "web"
        # 用户id
        uid = "57a358dc8ac247005f16735b"
        # token
        token = "eyJhY2Nlc3NfdG9rZW4iOiJsbklETEdSU2RjajRPc29SIiwicmVmcmVzaF90b2tlbiI6Ik5RajNGTDc1Z3Bwd1o5OU8iLCJ0b2tlbl90eXBlIjoibWFjIiwiZXhwaXJlX2luIjoyNTkyMDAwfQ=="
        # 设备id
        device_id = "1534834849402"
        # 全部热门
        url = "https://timeline-merger-ms.juejin.im/v1/get_entry_by_rank"
        param = {
            'src': src,
            'uid': uid,
            'token': token,
            'limit': 20,
            'device_id': device_id,
            'category': "all",
            'recomment': 1
        }
        # 后端本周热门
        urlBackend = "https://timeline-merger-ms.juejin.im/v1/get_entry_by_period"
        paramBackend = {
            'src': src,
            'uid': uid,
            'token': token,
            'limit': 20,
            'device_id': device_id,
            'category': "5562b419e4b00c57d9b94ae2",
            'recomment': 1,
            'period': 'week'
        }
        self._craw(url, param, 40)
        self._craw(urlBackend, paramBackend, 30)
