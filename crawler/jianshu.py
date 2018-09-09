# -*- coding: utf-8 -*-
import requests
import arrow

from base.crawler import Crawler
from base.third_post import ThirdPost
from conf.logger import log
from db.third_post_db import third_post_db

headers = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    "Connection": "keep-alive",
    "Cookie": "read_mode=day; default_font=font2; locale=zh-CN; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1535546099,1535556627,1535612856,1535895145; remember_user_token=W1syNjMxODIzXSwiJDJhJDEwJHh4VS9JR3dHTGdpYk8wQTgxTDRzcy4iLCIxNTM1ODk1MjQ1LjY3NjA4MSJd--118c26ae7eb548ac928622ad299202a7f1092df8; _m7e_session=8afaf2a40989d2405aa45560db8701cd; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%222631823%22%2C%22%24device_id%22%3A%2216351e1d7f06f5-0c78b4667ea057-33627f06-1296000-16351e1d7f14ef%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_utm_source%22%3A%22desktop%22%2C%22%24latest_utm_medium%22%3A%22index-collections%22%2C%22%24latest_utm_campaign%22%3A%22maleskine%22%2C%22%24latest_utm_content%22%3A%22note%22%7D%2C%22first_id%22%3A%2216351e1d7f06f5-0c78b4667ea057-33627f06-1296000-16351e1d7f14ef%22%7D; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1535896571",
    "Host": "www.jianshu.com",
    "Referer": "https://www.jianshu.com/c/addfce4ca518",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
}


class JianShu(Crawler):

    def __init__(self):
        super().__init__()
        self.third_id = 8
        self.third_name = "简书"

    def _craw(self, url, param=None, *args):
        while True:
            res = requests.get(url, params=param, headers=headers)
            param["page"] = param["page"] + 1
            if res.status_code == 200:
                # response
                body_json = res.json()
                print(len(body_json))
                if body_json:
                    res_list = []
                    for arti in body_json:
                        arti = arti['object']['data']
                        data = third_post_db.find_by_pt_id(arti['id'], self.third_id)
                        if data is None:  # 大于30喜欢的加入
                            # 构建
                            post = ThirdPost(self.third_id, self.third_name,0)
                            post.tags = param["tags"]
                            # 顺序 文章id、标题、标签、作者、喜欢数、评论数、跳转url、创建时间
                            post.post_id = arti['id']
                            post.title = arti['title']
                            post.author = arti['user']['nickname']
                            post.content = arti['public_abbr']
                            post.like_num = arti['likes_count']
                            post.comment_num = arti['public_comments_count']
                            post.redirect_url = 'https://www.jianshu.com/p/' + arti["slug"]
                            post.creatime = arrow.get(
                                arti['first_shared_at']).format('YYYY-MM-DD HH:mm:ss')
                            res_list.append(post)
                    log.info("[%s]爬取-> %s  %d条记录", self.third_name, url, len(res_list))
                    self.batch_insert(res_list)
                else:
                    break

    def start(self):
        ## 简书专题
        # java进阶干货
        url1 = "https://www.jianshu.com/asimov/collections/slug/addfce4ca518/public_notes"
        # 深入浅出golang
        url2 = "https://www.jianshu.com/asimov/collections/slug/490b2e276912/public_notes"
        # elasticsearch
        url3 = "https://www.jianshu.com/asimov/collections/slug/c802bfa8b60e/public_notes"
        # 数据结构和算法
        url4 = "https://www.jianshu.com/asimov/collections/slug/2e97444f8079/public_notes"
        # leetcode
        url5 = "https://www.jianshu.com/asimov/collections/slug/b43cdd926c76/public_notes"
        # 技术干货
        url6 = "https://www.jianshu.com/asimov/collections/slug/38d96caffb2f/public_notes"
        # 分布式架构
        url7 = "https://www.jianshu.com/asimov/collections/slug/3f476518d832/public_notes"
        # golang
        url8 = "https://www.jianshu.com/asimov/collections/slug/3e489dead7a7/public_notes"
        # spring
        url9 = "https://www.jianshu.com/asimov/collections/slug/f0cf6eae1754/public_notes"
        # 部署运维
        url10 = "https://www.jianshu.com/asimov/collections/slug/5484c13010a0/public_notes"
        # javascript进阶营
        url11 = "https://www.jianshu.com/asimov/collections/slug/f63dac4d430e/public_notes"
        param1 = {
            "page": 1,
            "count": 10,
            "order_by": "added_at",
            "tags": "前端"
        }
        self._craw(url11, param1)
