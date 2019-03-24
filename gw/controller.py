import requests
import sys
import html2text
from flask import Flask, request
import urllib.parse
from base import scheduled
import html
from bs4 import BeautifulSoup
from conf.logger import log
import re
import json
from util import myos

app = Flask(__name__)

h = html2text.HTML2Text()
# html to markdown

infoq_headers = {
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

segment_headers = {
    'authority': 'segmentfault.com',
    'method': 'GET',
    'path': '/a/1190000018604138',
    'scheme': 'https',
    'accept': 'text/html, application/xhtml+xml, application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age = 0',
    'cookie': '_ga=GA1.2.999831881.1526098418; PHPSESSID=web1~h6kd4m66rlhv83f0sof283p58j; _gid=GA1.2.641619629.1553329489; _gat=1; Hm_lvt_e23800c454aa573c0ccb16b52665ac26=1552999110,1553058348,1553329489,1553396821; Hm_lpvt_e23800c454aa573c0ccb16b52665ac26=1553396847',
    'referer': 'https://segmentfault.com/',
    'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}


@app.route('/html2Markdown')
def getpicurl():

    third_type = request.args.get('thirdType')
    url = request.args.get('url')
    third_type = int(third_type)
    if third_type == 1:
        return juejin(url)
    if third_type == 4:
        return cnblog(url)
    if third_type == 5:
        return importNew(url)
    if third_type == 10:
        return segment(url)
    if third_type == 11:
        return infoq(url)
    return ""


def juejin(url):

    res = requests.get(url).json()
    if res['s'] != 1:
        return ''
    s = res['d']['content']
    r = h.handle(s)
    return r


def infoq(url):
    # infoq url 就是id
    param = {
        "uuid": url
    }
    res = requests.post('https://www.infoq.cn/public/v1/article/getDetail',
                        json.dumps(param), headers=infoq_headers).json()
    s = res['data']['content']
    r = h.handle(s)
    return r


def segment(url):

    proxy = myos.get_proxy()
    log.info("user proxy %s", proxy)
    res = requests.get(url, headers=segment_headers, proxies={
                       'http': "http://".format(proxy)})
    # html文档
    htmls = res.text
    soup = BeautifulSoup(htmls, 'html.parser')

    article = soup.find("div", class_="article__content")
    imgList = article.find_all("img")
    for img in imgList:
        url_str = "https://www.chaoyer.com/csy/common/file/proxy?proxy=1&img=https://segmentfault.com" + str(
            img["data-src"])
        img_res = requests.get(url_str)
        img["src"] = eval(img_res.text.strip())
    s = article.prettify()
    r = h.handle(s)
    return r


def importNew(url):
    res = requests.get(url)

    # html文档
    htmls = res.text
    # print(s)
    h = html2text.HTML2Text()
    soup = BeautifulSoup(htmls, 'html.parser')

    article = soup.find("div", class_="entry")
    s = article.prettify()
    r = h.handle(s)
    return r


def cnblog(url):
    res = requests.get(url)
    # html文档
    htmls = res.text
    h = html2text.HTML2Text()
    soup = BeautifulSoup(htmls, 'html.parser')

    article = soup.find("div", id="cnblogs_post_body")
    s = article.prettify()
    r = h.handle(s)
    return r


def init():
    scheduled.start(app)
    app.run(host='0.0.0.0', port=8001, debug=False)
