# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import datetime

from base.crawler import Crawler
from base.third_post import ThirdPost
from db.third_post_db import third_post_db
from conf.logger import log

# 推酷爬虫  创建时间2018-05-17
host = "https://www.tuicool.com"

class TuiKu(Crawler):

    def _craw(self, url, param=None, *args):

        res = requests.get(url)
        if res.status_code == 200:

            # html文档
            html = res.text
            soup = BeautifulSoup(html, "html.parser")

            # 所有的文章
            posts = soup.find_all("div", class_="list_article_item")
            res_list = []

            # 多个文章解析
            for post in posts:

                p = ThirdPost(self.third_id, self.third_name,0)

                tip_spans = post.find("div", class_="tip").find_all("span")

                # postId
                p.post_id = post['data-id']
                # 标题
                p.title = post.find("div", class_="title").a.string
                # 跳转路由
                p.redirect_url = host + post.find("div", class_="title").a['href']
                # 创建时间
                now_year = datetime.datetime.now().year
                p.creatime = str(now_year) + "-" + list(tip_spans)[2].string.strip()
                # 作者
                p.author = list(tip_spans)[0].string.strip()
                # 标签
                p.tags = args[0]

                data = third_post_db.find_by_pt_id(p.post_id, p.third_id)
                if data is None:
                    res_list.append(p)

            log.info("[%s]爬取-> %s  %d条记录", self.third_name, url, len(res_list))
            self.batch_insert(res_list)

    def start(self):
        url = "https://www.tuicool.com/topics/11000072?st=1&lang=1&pn=0"
        self._craw(url, None, "JAVA后端")
        url1 = "https://www.tuicool.com/topics/11130000?st=1&lang=1"
        self._craw(url1, None, "Python")
        url2 = "https://www.tuicool.com/topics/11060028?st=1&lang=1"
        self._craw(url2, None, "NodeJs")
        url5 = "https://www.tuicool.com/topics/11080084?st=1&lang=1"
        self._craw(url5, None, "Golang")

    def __init__(self):
        super().__init__()
        self.third_id = 3
        self.third_name = "推酷"
