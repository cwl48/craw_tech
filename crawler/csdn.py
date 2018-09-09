# -*- coding: utf-8 -*-
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


class Csdn(Crawler):

    def __init__(self):
        super().__init__()
        self.third_id = 9
        self.third_name = "CSDN"
        self.can_analysis = 1

    def _craw(self, url, param=None, *args):
        res = requests.get(url)
        if res.status_code == 200:
            # html文档
            htmls = res.text
            soup = BeautifulSoup(htmls, 'html.parser')
            # 解析出页码数
            total_box = soup.find("div", class_="statistics_t")
            total = int(total_box.find("span").text)
            total_page = int(math.ceil(total / 20))
            # 一页一页爬取
            index = 1
            while total_page >= 1 and index <= total_page:
                article_list = []
                param = {
                    "page": index
                }
                res = requests.get(url, param)
                if res.status_code == 200:
                    # htmls文档
                    htmls = res.text
                    soup = BeautifulSoup(htmls, 'html.parser')
                    detail_list = soup.find("ul", class_="detail_list").find_all("li")
                    for detail in detail_list:
                        href = detail.find("a")["href"]
                        article_list.append(href)

                    res_list = []
                    log.info("该专题有%s篇文章", len(article_list))

                    for i, article in enumerate(article_list):

                        log.info("%s-->%d", article, i+1)
                        res = requests.get(article)
                        if res.status_code == 200:
                            # htmls文档
                            htmls = res.text
                            soup = BeautifulSoup(htmls, 'html.parser')

                            p = ThirdPost(self.third_id, self.third_name, self.can_analysis)
                            p.redirect_url = article
                            p.post_id = re.findall(r"/article/(.+)", p.redirect_url)[0]
                            p.title = soup.find("h1", class_="title-article").text
                            p.author = soup.find("a", id="uid").text
                            # 文章内容
                            a = soup.find("article")
                            # 查看更多和版权信息删除
                            ar = a.find("div", class_="article-copyright")
                            hide = a.find("div", class_="hide-article-box")
                            if hide is not None:
                                hide.replace_with("")
                            if ar is not None:
                                ar.replace_with("")
                            # url 解决反盗链
                            imgList = a.find_all("img")
                            for img in imgList:
                                url_str = "https://www.chaoyer.com/api/file/proxy?proxy=https://blog.csdn.net&img=" + str(
                                    img["src"])
                                img["src"] = url_str
                                p.content = html.escape((str(a)))
                            p.creatime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            data = third_post_db.find_by_pt_id(p.post_id, p.third_id)
                            if data is None:
                                res_list.append(p)
                    log.info("[%s]爬取-> %s   %d条记录", self.third_name, url, len(res_list))
                    self.batch_insert(res_list)
                    index = index + 1

    def start(self):
        # url = "https://blog.csdn.net/column/details/chenssy-design.html"
        # url = "https://blog.csdn.net/column/details/14531.html"
        # url = "https://blog.csdn.net/column/details/15500.html"
        # url = "https://blog.csdn.net/column/details/16165.html"
        # url = "https://blog.csdn.net/column/details/deep-elasticsearch.html"
        # url = "https://blog.csdn.net/column/details/elasticsearch-action.html"
        url = "https://blog.csdn.net/column/details/redis330.html"
        self._craw(url)
