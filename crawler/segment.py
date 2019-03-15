import html
import math
import re
from datetime import datetime

import pymysql
import requests
import arrow

from base.crawler import Crawler
from bs4 import BeautifulSoup
from base.third_post import ThirdPost
from conf.logger import log
from db.third_post_db import third_post_db


host = 'https://segmentfault.com'


class Segment(Crawler):

    def __init__(self):
        super().__init__()
        self.third_id = 10
        self.third_name = "Segment"

    def _craw(self, url, param=None, *args):
        res = requests.get(url)
        if res.status_code == 200:
            # html文档
            htmls = res.text
            soup = BeautifulSoup(htmls, 'html.parser')
            news_list = soup.find("div", class_="news-list")
            # 所有的文章
            posts = news_list.find_all("div", class_="news-item")

            res_list = []

            for post in posts:

                p = ThirdPost(self.third_id, self.third_name, 0)

                post_title = post.find("h4", "news__item-title")
                p.title = post_title.text

                post_href = post.find("a", target="_blank")
                p.redirect_url = host+post_href['href']

                post_author = post.find("span", class_="author")
                p.author = post_author.a.text
                # 是SegmentFault不
                if p.author == "SegmentFault":
                    continue
                # 创建时间
                p.creatime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # postId
                p.post_id = "segment-"+post_href['href']
                # content
                p.content = post.find(
                    "div", class_="article-excerpt").text.strip()
                data = third_post_db.find_by_pt_id(p.post_id, p.third_id)
                if data is None:
                    res_list.append(p)
            log.info("[%s]爬取-> %s   %d条记录",
                     self.third_name, url, len(res_list))
            self.batch_insert(res_list)

    def start(self):
        self._craw("https://segmentfault.com/hottest")


def start():
    Segment().start()
