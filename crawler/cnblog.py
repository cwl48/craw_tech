# -*- coding: utf-8 -*-
import requests

from base.crawler import Crawler
from base.third_post import ThirdPost
from bs4 import BeautifulSoup
import re

from db.third_post_db import third_post_db
from conf.logger import log

# 博客园爬虫  创建时间2018-05-18

class CnBlog(Crawler):

    def __init__(self):
        super().__init__()
        self.third_id = 4
        self.third_name = "博客园"

    def _craw(self, url, param=None, *args):
        res = requests.post(url, param)
        if res.status_code == 200:

            # html文档
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')
            # 所有的文章
            posts = soup.find_all("div", class_="post_item")

            res_list = []
            for post in posts:

                p = ThirdPost(self.third_id, self.third_name,0)
                post_a = post.find("a", class_="titlelnk")
                #  # 跳转路由
                p.redirect_url = post_a['href']
                # postId
                p.post_id = re.findall(r"/p/(.+?)\.html", p.redirect_url)[0]
                # title
                p.title = post_a.string
                # 创建时间
                p.creatime = post_a.next_sibling.string

                data = third_post_db.find_by_pt_id(p.post_id, p.third_id)
                if data is None:
                    res_list.append(p)
            log.info("[%s]爬取-> %s  %d条记录", self.third_name, url, len(res_list))
            self.batch_insert(res_list)

    def start(self):
        url = "https://www.cnblogs.com/aggsite/HeadlineList"
        self._craw(url, {"PageIndex": 1})
