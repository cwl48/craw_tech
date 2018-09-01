# -*- coding: utf-8 -*-
import requests

from base.crawler import Crawler
from base.third_post import ThirdPost
from bs4 import BeautifulSoup
from conf.logger import log

# 开发者头条
# 创建时间2018-05-16
from db.third_post_db import third_post_db

host = "https://toutiao.io"

url7 = "https://toutiao.io/posts/hot/7"
url30 = "https://toutiao.io/posts/hot/30"
url90 = "https://toutiao.io/posts/hot/90"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'toutiao.io',
    'Referer': 'https://toutiao.io/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}


class KaiFaTouTiao(Crawler):

    def __init__(self):
        super().__init__()
        self.third_name = "开发者头条"
        self.third_id = 2

    def _craw(self, url, param=None, *args):
        res = requests.get(url, None, headers=headers)
        if res.status_code == 200:

            # html文档
            html = res.text
            soup = BeautifulSoup(html, "html.parser")
            # 所有的文章
            posts = soup.find_all("div", class_="post")

            res_list = []
            # 多个文章解析
            for post in posts:

                p = ThirdPost(self.third_id, self.third_name)
                post_content = post.find("div", class_="content")
                meta = post_content.find("div", class_="meta")
                user_info = post.find(
                    "div", class_="user-info").find("div", class_="user-avatar")
                # postId
                p.post_id = post_content.p.a["href"]
                # 标题
                p.title = post_content.h3.a.string
                # 内容
                p.content = post_content.p.a.string
                # 赞数量
                p.like_num = post.find("a", class_="like-button").find("span").string
                # 评论数量
                p.comment_num = list(meta.find("span").stripped_strings)[0]
                # 跳转路由
                p.redirect_url = host + post_content.h3.a['href']
                # 作者
                p.author = user_info.a["title"].split("-")[0]

                data = third_post_db.find_by_pt_id(p.title)
                if data is None:
                    res_list.append(p)
            log.info("[%s]爬取-> %s  %d条记录", self.third_name, url, len(res_list))
            self.batch_insert(res_list)

    def start(self):
        self._craw(url7)
        self._craw(url30)
        self._craw(url90)
