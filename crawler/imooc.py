# -*- coding: utf-8 -*-
import requests
import arrow
from bs4 import BeautifulSoup
from datetime import datetime
import time

from base.crawler import Crawler
from base.third_post import ThirdPost
from db.third_post_db import third_post_db
from conf.logger import log

host = 'https://www.imooc.com'


class Imooc(Crawler):

    def __init__(self):
        super().__init__()
        self.third_id = 6
        self.third_name = "慕课网"

    def _craw(self, url, param=None, *args):

        res = requests.get(url, param)
        if res.status_code == 200:

            # html文档
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')

            res_list = []

            # 所有的文章
            posts = soup.find_all("div", class_="article-lwrap")

            for post in posts:

                p = ThirdPost(self.third_id, self.third_name,0)

                post_a = post.find("a", "title")
                # 标题
                p.title = post_a.p.string
                # 跳转路由
                p.redirect_url = host+post_a['href']
                p.author = post.find("a", class_='nickName').string.strip()
                # 创建时间
                p.creatime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # postId
                p.post_id = "/imooc"+post_a['href']
                # tags
                p_skills = post.find("span", class_="skill")
                p_tags = p_skills.find_all("a")
                tags = []
                for tag in p_tags:
                    tags.append(tag.span.string)
                p.tags = ",".join(tags)
                data = third_post_db.find_by_pt_id(p.post_id, p.third_id)
                if data is None:
                    res_list.append(p)
            log.info("[%s]爬取-> %s   %d条记录",
                     self.third_name, url, len(res_list))
            self.batch_insert(res_list)

    def start(self):
        url1 = "https://www.imooc.com/article/excellent?type=1"
        url2 = "https://www.imooc.com/article/excellent?type=2"
        self._craw(url1)
        self._craw(url2)
