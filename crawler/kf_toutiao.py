# -*- coding: utf-8 -*-
import requests
import math
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
        res = requests.get(url, param, headers=headers)
        if res.status_code == 200:

            # html文档
            html = res.text
            soup = BeautifulSoup(html, "html.parser")
            # 所有的文章
            posts = soup.find_all("div", class_="post")
            # 作者
            author_wrap = soup.find("div", class_="m-b").h3.text
            res_list = []
            # 多个文章解析
            for post in posts:
                p = ThirdPost(self.third_id, self.third_name, 0)
                post_content = post.find("div", class_="content")
                meta = post_content.find("div", class_="meta")
                if param == None:
                    user_info = post.find(
                        "div", class_="user-info").find("div", class_="user-avatar")
                    # 作者
                    p.author = user_info.a["title"].split("-")[0]
                    # postId
                    p.post_id = post_content.p.a["href"]
                    # 内容
                    p.content = post_content.p.a.string
                else:
                    p.author = author_wrap
                    # postId
                    p.post_id = post_content["data-url"]
                    p.content = ""
                # 标题
                p.title = post_content.h3.a.string
                # 赞数量
                p.like_num = post.find(
                    "a", class_="like-button").find("span").string
                # 评论数量
                p.comment_num = list(meta.find("span").stripped_strings)[0]
                # 跳转路由
                p.redirect_url = host + post_content.h3.a['href']

                data = third_post_db.find_by_pt_id(p.post_id, p.third_id)
                if data is None:
                    res_list.append(p)
            log.info("[%s]爬取-> %s  %d条记录", self.third_name, url, len(res_list))
            self.batch_insert(res_list)

    def _craw_with_page(self, url):
        res = requests.get(url, None, headers=headers)

        if res.status_code == 200:
            # html文档
            html = res.text
            soup = BeautifulSoup(html, "html.parser")
            countStr = soup.find("span", class_="count").text
            total_page = int(math.ceil(int(countStr) / 25))
            index = 1
            while total_page >= 1 and index <= total_page:
                param = {
                    "page": index
                }
                self._craw(url, param)
                index = index+1

    def start(self):
        # 热门分享
        self._craw(url7)
        self._craw(url30)
        self._craw(url90)
        # 独家号
        # 码洞
        # self._craw_with_page("https://toutiao.io/subjects/321918")

        # # 文野
        # self._craw_with_page("https://toutiao.io/subjects/135973")

        # # Java后端技术
        # self._craw_with_page("https://toutiao.io/subjects/63673")

        # # 基础架构自留地
        # self._craw_with_page("https://toutiao.io/subjects/26578")

        # # 技术分享小站
        # self._craw_with_page("https://toutiao.io/subjects/12684")

        # # JAVA程序员技术分享
        # self._craw_with_page("https://toutiao.io/subjects/1996")

        # # redis
        # self._craw_with_page("https://toutiao.io/subjects/46756")

        # # 进击的架构师
        # self._craw_with_page("https://toutiao.io/subjects/101482")

        # # 美团
        # self._craw_with_page("https://toutiao.io/subjects/117027")

        # # 魅族
        # self._craw_with_page("https://toutiao.io/subjects/22029")

        # # 技术小黑屋
        # self._craw_with_page("https://toutiao.io/subjects/117")

        # # 架构之美
        # self._craw_with_page("https://toutiao.io/subjects/42200")

        # # Linux中国
        # self._craw_with_page("https://toutiao.io/subjects/10795")

        # # JAVA干货
        # self._craw_with_page("https://toutiao.io/subjects/51515")

        # # python 之美
        # self._craw_with_page("https://toutiao.io/subjects/6988")

        # # coding技术
        # self._craw_with_page("https://toutiao.io/subjects/14483")

        # # 程序员的朋友圈
        # self._craw_with_page("https://toutiao.io/subjects/378")

        # # 彻底理解计算机
        # self._craw_with_page("https://toutiao.io/subjects/2356")

        # # docker
        # self._craw_with_page("https://toutiao.io/subjects/21")

        # # 前端杂谈
        # self._craw_with_page("https://toutiao.io/subjects/6782")

        # # 前端js
        # self._craw_with_page("https://toutiao.io/subjects/11510")

        # # 后端技术杂谈
        # self._craw_with_page("https://toutiao.io/subjects/4944")

        # # 程序员学架构
        # self._craw_with_page("https://toutiao.io/subjects/589")

        # # 高性能高并发高可用
        # self._craw_with_page("https://toutiao.io/subjects/4755")

        # # 深入浅出es6
        # self._craw_with_page("https://toutiao.io/subjects/1221")

        # # 原创技术经验
        # self._craw_with_page("https://toutiao.io/subjects/24410")

        # # 第八个手艺人
        # self._craw_with_page("https://toutiao.io/subjects/523")

        # # Python中文社区
        # self._craw_with_page("https://toutiao.io/subjects/183367")

        # # 运维精选
        # self._craw_with_page("https://toutiao.io/subjects/206")

        # # 开源中国推荐博客
        # self._craw_with_page("https://toutiao.io/subjects/42648")

        # # app后端开发
        # self._craw_with_page("https://toutiao.io/subjects/50375")

        # # 信息安全
        # self._craw_with_page("https://toutiao.io/subjects/30718")

        # # 开源中国技术翻译
        # self._craw_with_page("https://toutiao.io/subjects/42628")

        # # 牛客网精华贴
        # self._craw_with_page("https://toutiao.io/subjects/17560")

        # # 算法那些事
        # self._craw_with_page("https://toutiao.io/subjects/42007")

        # # 前端与nodejs
        # self._craw_with_page("https://toutiao.io/subjects/7076")

        # # React vue 学习
        # self._craw_with_page("https://toutiao.io/subjects/1145")

        # # 前端stepbystep
        # self._craw_with_page("https://toutiao.io/subjects/29096")

        # # java实战技术
        # self._craw_with_page("https://toutiao.io/subjects/22887")

        # # 前端早读课
        # self._craw_with_page("https://toutiao.io/subjects/11907")

        # # segmentFault 优质内容
        # self._craw_with_page("https://toutiao.io/subjects/50525")

        # # ML之道
        # self._craw_with_page("https://toutiao.io/subjects/42203")

        # # 阿里中间件
        # self._craw_with_page("https://toutiao.io/subjects/108495")

        # # 互联网公司架构
        # self._craw_with_page("https://toutiao.io/subjects/132303")

        # # golang开发
        # self._craw_with_page("https://toutiao.io/subjects/47783")

        # # tomcat 那些事
        # self._craw_with_page("https://toutiao.io/subjects/53054")

        # # 小弧光黑板报
        # self._craw_with_page("https://toutiao.io/subjects/458")

        # # 分布式系统
        # self._craw_with_page("https://toutiao.io/subjects/8411")

        # # nodejs
        # self._craw_with_page("https://toutiao.io/subjects/75893")

        # # 江南布衣
        # self._craw_with_page("https://toutiao.io/subjects/2147")

        # # java进阶
        # self._craw_with_page("https://toutiao.io/subjects/56996")

        # # 腾讯bugly干货分享
        # self._craw_with_page("https://toutiao.io/subjects/66980")

        # # GO夜读
        # self._craw_with_page("https://toutiao.io/subjects/18894")

        # # 死磕java
        # self._craw_with_page("https://toutiao.io/subjects/25239")

        # # 分布式系统架构
        # self._craw_with_page("https://toutiao.io/subjects/132474")

        # # 只有干货
        # self._craw_with_page("https://toutiao.io/subjects/20338")

        # # go
        # self._craw_with_page("https://toutiao.io/subjects/18464")

        # # 一个程序员的自我修养
        # self._craw_with_page("https://toutiao.io/subjects/35168")

        # # 七牛
        # self._craw_with_page("https://toutiao.io/subjects/111688")

        # # 服务端分享
        # self._craw_with_page("https://toutiao.io/subjects/991")

        # # java 后端
        # self._craw_with_page("https://toutiao.io/subjects/132961")

        # # 游戏开发杂货铺
        # self._craw_with_page("https://toutiao.io/subjects/528")

        # # unity
        # self._craw_with_page("https://toutiao.io/subjects/91210")

        # # 黄哥的python短文
        # self._craw_with_page("https://toutiao.io/subjects/35888")

        # # 花满楼
        # self._craw_with_page("https://toutiao.io/subjects/913")

        # # 携程技术
        # self._craw_with_page("https://toutiao.io/subjects/119893")

        # # 吴说
        # self._craw_with_page("https://toutiao.io/subjects/2833")

        # # netty技术内幕
        # self._craw_with_page("https://toutiao.io/subjects/183692")

        # # 2048
        # self._craw_with_page("https://toutiao.io/subjects/3216")

        # # 一亩三分地
        # self._craw_with_page("https://toutiao.io/subjects/796")

        # # 58同程技术团队
        # self._craw_with_page("https://toutiao.io/subjects/260377")

        # # eggjs技术团队
        # self._craw_with_page("https://toutiao.io/subjects/17491")

        # # 开发者独家号
        # self._craw_with_page("https://toutiao.io/subjects/13080")

        # # holys的分享
        # self._craw_with_page("https://toutiao.io/subjects/642")

        # # 游戏开发和后端开发那些事
        # self._craw_with_page("https://toutiao.io/subjects/162233")

        # # 死磕elasticsearch
        # self._craw_with_page("https://toutiao.io/subjects/272620")

        # # 即时通讯网
        # self._craw_with_page("https://toutiao.io/subjects/104810")

        # # 计算机文章翻译
        # self._craw_with_page("https://toutiao.io/subjects/136271")

        # # 雨痕学堂
        # self._craw_with_page("https://toutiao.io/subjects/41005")

        # # 唯品会
        # self._craw_with_page("https://toutiao.io/subjects/41005")

        # # 承香墨影 android
        # self._craw_with_page("https://toutiao.io/subjects/16900")

        # # android & ios工程师之路
        # self._craw_with_page("https://toutiao.io/subjects/4829")

        # # 迷路的程序员
        # self._craw_with_page("https://toutiao.io/subjects/161574")

        # # 技术杂谈
        # self._craw_with_page("https://toutiao.io/subjects/5207")

        # # 从前端到全栈
        # self._craw_with_page("https://toutiao.io/subjects/149476")

        # # IT招式和内功修养
        # self._craw_with_page("https://toutiao.io/subjects/58552")

        # # 全栈头条
        # self._craw_with_page("https://toutiao.io/subjects/135469")

        # # 阿里中间件博客
        # self._craw_with_page("https://toutiao.io/subjects/108495")

        # # 走向架构师之路
        # self._craw_with_page("https://toutiao.io/subjects/236468")

        # # fir.im Weekly
        # self._craw_with_page("https://toutiao.io/subjects/14908")

        # # 互联网公司架构方案
        # self._craw_with_page("https://toutiao.io/subjects/132303")

        # # 有赞技术精选
        # self._craw_with_page("https://toutiao.io/subjects/86994")

        # # 高效运维
        # self._craw_with_page("https://toutiao.io/subjects/95610")

        # # Dbaplus.cn精选文章
        # self._craw_with_page("https://toutiao.io/subjects/87719")

        # # sunsky303
        # self._craw_with_page("https://toutiao.io/subjects/48071")

        # # Coder at Work
        # self._craw_with_page("https://toutiao.io/subjects/97282")

        # # 芋道源码
        # self._craw_with_page("https://toutiao.io/subjects/2019")

        # # 大数据生态
        # self._craw_with_page("https://toutiao.io/subjects/136176")

        # # 浪客用react,java全栈
        # self._craw_with_page("https://toutiao.io/subjects/132403")

        # # 数据淘金
        # self._craw_with_page("https://toutiao.io/subjects/120437")

        # # 进击的程序猿
        # self._craw_with_page("https://toutiao.io/subjects/24912")

        # # 274970的独家号
        # self._craw_with_page("https://toutiao.io/subjects/151363")

        # # Java深度&人工智能（只发原创）
        # self._craw_with_page("https://toutiao.io/subjects/195885")

        # # 最佳实践
        # self._craw_with_page("https://toutiao.io/subjects/72425")

        # # 微信公众号:笑你妹呀
        # self._craw_with_page("https://toutiao.io/subjects/242796")

        # # 七牛云
        # self._craw_with_page("https://toutiao.io/subjects/111688")

        # # 悦读集
        # self._craw_with_page("https://toutiao.io/subjects/105609")

        # # ThoughtWorks
        # self._craw_with_page("https://toutiao.io/subjects/8973")

        # # 1码平川的独家号
        # self._craw_with_page("https://toutiao.io/subjects/164069")

        # # 落北的mark簿
        # self._craw_with_page("https://toutiao.io/subjects/123823")

        # # 瞬息之间
        # self._craw_with_page("https://toutiao.io/subjects/50961")

        # # 虞大胆的叽叽咋咋
        # self._craw_with_page("https://toutiao.io/subjects/133323")

        # # 白帽子
        # self._craw_with_page("https://toutiao.io/subjects/3838")

        # # Scala & Java
        # self._craw_with_page("https://toutiao.io/subjects/190184")

        # # ScalaCool
        # self._craw_with_page("https://toutiao.io/subjects/180363")

        # # 码个蛋
        # self._craw_with_page("https://toutiao.io/subjects/102848")

        # # Awesomes-cn
        # self._craw_with_page("https://toutiao.io/subjects/27538")

        # # 终端研发部
        # self._craw_with_page("https://toutiao.io/subjects/257104")
