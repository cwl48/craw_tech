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
import time
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

jianshu_headers = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    "Connection": "keep-alive",
    "Cookie": "read_mode=day; default_font=font2; locale=zh-CN; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1535546099,1535556627,1535612856,1535895145; remember_user_token=W1syNjMxODIzXSwiJDJhJDEwJHh4VS9JR3dHTGdpYk8wQTgxTDRzcy4iLCIxNTM1ODk1MjQ1LjY3NjA4MSJd--118c26ae7eb548ac928622ad299202a7f1092df8; _m7e_session=8afaf2a40989d2405aa45560db8701cd; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%222631823%22%2C%22%24device_id%22%3A%2216351e1d7f06f5-0c78b4667ea057-33627f06-1296000-16351e1d7f14ef%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_utm_source%22%3A%22desktop%22%2C%22%24latest_utm_medium%22%3A%22index-collections%22%2C%22%24latest_utm_campaign%22%3A%22maleskine%22%2C%22%24latest_utm_content%22%3A%22note%22%7D%2C%22first_id%22%3A%2216351e1d7f06f5-0c78b4667ea057-33627f06-1296000-16351e1d7f14ef%22%7D; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1535896571",
    "Host": "www.jianshu.com",
    "Referer": "https://www.jianshu.com/c/addfce4ca518",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
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
    if third_type == 8:
        return jianshu(url)
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


def jianshu(url):

    res = requests.get(url, headers=jianshu_headers)
    # html文档
    htmls = res.text

    h = html2text.HTML2Text()
    soup = BeautifulSoup(htmls, 'html.parser')

    article = soup.find("div", class_="show-content-free")
    imgList = article.find_all("img")
    for img in imgList:
        url_str = "https:"+str(img["data-original-src"])
        img["src"] = url_str

    s = article.prettify()
    r = h.handle(s)
    return r


def segment(url):
    res = requests.get(url, headers=segment_headers)
    # html文档
    htmls = res.text
    soup = BeautifulSoup(htmls, 'html.parser')

    article = soup.find("div", class_="article__content")
    if article == None:
        return ""
    imgList = article.find_all("img")
    for img in imgList:
        url_str = "http://localhost:8000/common/file/proxy?proxy=1&img=https://segmentfault.com" + str(
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

    imgList = article.find_all("img")
    for img in imgList:
        url_str = "http://localhost:8000/common/file/proxy?proxy=2&img=" + str(
            img["src"])
        img_res = requests.get(url_str)
        img["src"] = eval(img_res.text.strip())
    s = article.prettify()
    r = h.handle(s)
    return r


def init():
    scheduled.start(app)
    app.run(host='0.0.0.0', port=8001, debug=False)
