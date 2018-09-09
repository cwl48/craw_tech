# -*- coding: utf-8 -*-
import requests

from base.crawler import Crawler
from base.third_post import ThirdPost
from bs4 import BeautifulSoup
import re

from db.third_post_db import third_post_db
from conf.logger import log

# importNew 爬虫 创建时间 2018-05-191
class ImportNew(Crawler):

    def __init__(self):
        super().__init__()
        self.third_id = 5
        self.third_name = "importNew"

    def _craw(self, url, param=None, *args):

        res = requests.post(url)

        if res.status_code == 200:

            # html文档
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')

            res_list = []

            # 所有的文章
            archive = soup.find("div", id="archive")
            posts = archive.find_all("div", class_="post")
            for post in posts:

                p = ThirdPost(self.third_id, self.third_name,0)

                post_meta = post.find("div", class_="post-meta")
                post_a = post_meta.find("a", "meta-title")
                # 跳转路由
                p.redirect_url = post_a['href']
                # postId
                p.post_id = re.findall(r"m/(.+?)\.html", p.redirect_url)[0]
                # 标题
                p.title = post_a.string
                # 默认平台名
                p.author = self.third_name
                # 创建时间
                p.creatime = post_a.next_sibling.next_sibling.split("|")[0].strip()
                # 内容
                p.content = post.find("span", class_="excerpt").p.string
                if p.content is None:
                    p.content = ""
                data = third_post_db.find_by_pt_id(p.post_id, p.third_id)
                if data is None:
                    res_list.append(p)
            log.info("[%s]爬取-> %s   %d条记录", self.third_name, url, len(res_list))
            self.batch_insert(res_list)

    def start(self):
        url = "http://www.importnew.com/all-posts/page/"
        self._craw(url + str(1))
