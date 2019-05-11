# -*- coding: utf-8 -*-
import requests
import arrow
import json

from base.crawler import Crawler
from base.third_post import ThirdPost
from db.third_post_db import third_post_db
from conf.logger import log


header = {
    'Content-Type': 'application/json',
    'Origin': 'https://juejin.im',
    'Referer': 'https://juejin.im/timeline/recommended',
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'X-Agent': 'Juejin/Web',
    'X-Legacy-Device-Id': '1557555376151',
    'X-Legacy-Token': 'eyJhY2Nlc3NfdG9rZW4iOiJKdXU2WlJIQzVhU3F3dnRJIiwicmVmcmVzaF90b2tlbiI6IlhvUlhKeFVSa1NZc2RhTGkiLCJ0b2tlbl90eXBlIjoibWFjIiwiZXhwaXJlX2luIjoyNTkyMDAwfQ==',
    'X-Legacy-Uid': '57a358dc8ac247005f16735b'
}

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
        res = requests.post(url, json.dumps(param), headers=header)
        if res.status_code == 200:
            like_total = args[0]  # 至少喜欢的数量
            # juejin response
            body_json = res.json()
            print(body_json)
            if body_json['data'] is None:
                log.error("爬取掘金失败" + body_json['errors'])
                return
            article_list = body_json['data']['articleFeed']['items']['edges']

            res_list = []
            for artiCol in article_list:

                arti = artiCol['node']

                data = third_post_db.find_by_pt_id(
                    arti['id'], self.third_id)

                if data is None and arti['likeCount'] > like_total:  # 大于30喜欢的加入
                    # 构建
                    post = ThirdPost(self.third_id, self.third_name, 0)
                    tags = []
                    for t in arti['tags']:
                        tags.append(t['title'])
                    post.tags = ",".join(tags)
                    # 顺序 文章id、标题、标签、作者、喜欢数、评论数、跳转url、创建时间
                    post.post_id = arti['id']
                    post.title = arti['title']
                    post.author = arti['user']['username']
                    post.content = arti['content']
                    post.like_num = arti['likeCount']
                    post.comment_num = arti['commentsCount']
                    post.redirect_url = arti['originalUrl']
                    post.creatime = arrow.get(
                        arti['createdAt']).format('YYYY-MM-DD HH:mm:ss')

                    res_list.append(post)
            log.info("[%s]爬取-> %s  %d条记录", self.third_name, url, len(res_list))
            self.batch_insert(res_list)

    def start(self):
        # 全部热门
        url = "https://web-api.juejin.im/query"
        param = {
            "extensions": {
                "query": {
                    "id": "21207e9ddb1de777adeaca7a2fb38030"
                }
            },
            "operationName": "",
            "query": "",
            "variables": {
                     "first": 50,
                     "after": "",
                     "order": "POPULAR"
            }
        }
        # 后端本周热门
        paramBackend = {
            "extensions": {
                "query": {
                    "id": "21207e9ddb1de777adeaca7a2fb38030"
                }
            },
            "operationName": "",
            "query": "",
            "variables": {
                     "first": 50,
                     "after": "",
                     "category": "5562b419e4b00c57d9b94ae2",
                     "order": "POPULAR"
            }
        }
        # 前端本周热门
        paramFront = {
            "extensions": {
                "query": {
                    "id": "21207e9ddb1de777adeaca7a2fb38030"
                }
            },
            "operationName": "",
            "query": "",
            "variables": {
                     "first": 50,
                     "after": "",
                     "category": "5562b419e4b00c57d9b94ae2",
                     "order": "POPULAR"
            }
        }
        self._craw(url, param, 10)
        self._craw(url, paramBackend, 5)
        self._craw(url, paramFront, 5)


def start():
    JueJin().start()
