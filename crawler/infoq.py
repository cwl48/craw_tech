import html
import math
import re
from datetime import datetime

import pymysql
import requests
import arrow
import json
import time

from base.crawler import Crawler
from base.third_post import ThirdPost
from conf.logger import log
from db.third_post_db import third_post_db


host = 'https://www.infoq.cn/public/v1/my/recommond'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN, zh;q = 0.9, en;q = 0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Cookie': '_ga = GA1.2.764486653.1542099036;Hm_lvt_094d2af1d9a57fd9249b3fa259428445 = 1553218625;SERVERID = 1fa1f330efedec1559b3abbcb6e30f50 | 1553246716 | 1553246295;Hm_lpvt_094d2af1d9a57fd9249b3fa259428445 = 1553246716',
    'Host': 'www.infoq.cn',
    'Origin': 'https: // www.infoq.cn',
    'Referer': 'https: // www.infoq.cn /',
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'

}

score = arrow.now().timestamp


class InfoQ(Crawler):

    def __init__(self):
        super().__init__()
        self.third_id = 11
        self.third_name = "InfoQ"

    def _craw(self, url, param=None, *args):
        res = requests.post(url, json.dumps(param), headers=headers)
        if res.status_code == 200:
            # html文档
            body_json = res.json()
            print(body_json)

            article_list = body_json['data']
            res_list = []

            for post in article_list:

                p = ThirdPost(self.third_id, self.third_name, 0)

                p.title = post['article_title']

                tags = []
                for t in post['topic']:
                    tags.append(t['name'])
                p.tags = ",".join(tags)
                p.post_id = "infoq-"+post['uuid']
                if 'author' in post.keys():
                    p.author = post['author'][0]['nickname']
                else:
                    p.author = "InfoQ"
                p.content = post['article_summary']
                p.redirect_url = "https://www.infoq.cn/article/"+post['uuid']
                p.creatime = arrow.get(
                    post['utime']/1000).format('YYYY-MM-DD HH:mm:ss')
                data = third_post_db.find_by_pt_id(p.post_id, p.third_id)
                if data is None:
                    res_list.append(p)
            log.info("[%s]爬取-> %s   %d条记录",
                     self.third_name, url, len(res_list))
            self.batch_insert(res_list)

    def start(self):
        p = {
            "size": 50,
            "score": None
        }
        self._craw(host, p)


def start():
    InfoQ().start()
